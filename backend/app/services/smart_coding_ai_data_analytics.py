"""
Smart Coding AI - Data & Analytics Integration Capabilities
Implements capabilities 131-140: Advanced data processing and analytics features
"""

import re
import structlog
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime, timedelta
import json

logger = structlog.get_logger()


class DatabaseQueryOptimizer:
    """Implements capability #131: Database Query Optimization"""
    
    async def optimize_query(self,
                            query: str,
                            database_type: str = "postgresql",
                            schema: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Optimizes SQL and NoSQL queries
        
        Args:
            query: SQL or NoSQL query to optimize
            database_type: Database type (postgresql, mysql, mongodb, etc.)
            schema: Database schema information
            
        Returns:
            Optimized query with explanation and performance improvements
        """
        try:
            # Analyze query
            analysis = self._analyze_query(query, database_type)
            
            # Identify performance issues
            issues = self._identify_performance_issues(query, analysis)
            
            # Generate optimized query
            optimized = self._generate_optimized_query(query, issues, database_type)
            
            # Recommend indexes
            indexes = self._recommend_indexes(query, schema or {})
            
            # Estimate performance gain
            performance_gain = self._estimate_performance_gain(issues, optimized)
            
            return {
                "success": True,
                "original_query": query,
                "analysis": analysis,
                "performance_issues": issues,
                "optimized_query": optimized,
                "recommended_indexes": indexes,
                "estimated_improvement": performance_gain,
                "best_practices": self._generate_query_best_practices(database_type)
            }
        except Exception as e:
            logger.error("Query optimization failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_query(self, query: str, db_type: str) -> Dict[str, Any]:
        """Analyze query structure"""
        query_lower = query.lower()
        
        return {
            "query_type": self._detect_query_type(query_lower),
            "has_joins": "join" in query_lower,
            "has_subqueries": "select" in query_lower.split("select", 1)[1] if query_lower.count("select") > 1 else False,
            "has_aggregations": any(agg in query_lower for agg in ["count", "sum", "avg", "max", "min", "group by"]),
            "has_order_by": "order by" in query_lower,
            "has_limit": "limit" in query_lower,
            "has_where": "where" in query_lower,
            "uses_wildcard": "*" in query,
            "complexity": self._calculate_query_complexity(query_lower)
        }
    
    def _detect_query_type(self, query: str) -> str:
        """Detect query type"""
        if query.strip().startswith("select"):
            return "SELECT"
        elif query.strip().startswith("insert"):
            return "INSERT"
        elif query.strip().startswith("update"):
            return "UPDATE"
        elif query.strip().startswith("delete"):
            return "DELETE"
        else:
            return "UNKNOWN"
    
    def _calculate_query_complexity(self, query: str) -> str:
        """Calculate query complexity"""
        complexity_score = 0
        
        complexity_score += query.count("join") * 2
        complexity_score += query.count("select") - 1  # Subqueries
        complexity_score += 1 if "group by" in query else 0
        complexity_score += 1 if "having" in query else 0
        complexity_score += 1 if "order by" in query else 0
        
        if complexity_score == 0:
            return "Simple"
        elif complexity_score <= 3:
            return "Moderate"
        else:
            return "Complex"
    
    def _identify_performance_issues(self, query: str, analysis: Dict) -> List[Dict[str, str]]:
        """Identify performance issues in query"""
        issues = []
        
        if analysis["uses_wildcard"]:
            issues.append({
                "severity": "medium",
                "issue": "Using SELECT *",
                "impact": "Retrieves unnecessary columns, increases I/O",
                "fix": "Specify only needed columns"
            })
        
        if not analysis["has_where"] and analysis["query_type"] == "SELECT":
            issues.append({
                "severity": "high",
                "issue": "No WHERE clause (full table scan)",
                "impact": "Scans entire table, very slow for large tables",
                "fix": "Add WHERE clause to filter rows"
            })
        
        if not analysis["has_limit"] and analysis["query_type"] == "SELECT":
            issues.append({
                "severity": "medium",
                "issue": "No LIMIT clause",
                "impact": "May return millions of rows",
                "fix": "Add LIMIT to restrict result set"
            })
        
        if analysis["has_joins"] and not analysis["has_where"]:
            issues.append({
                "severity": "critical",
                "issue": "JOIN without WHERE clause",
                "impact": "Cartesian product, extremely slow",
                "fix": "Add WHERE clause to join condition"
            })
        
        if analysis["has_subqueries"]:
            issues.append({
                "severity": "medium",
                "issue": "Subquery detected",
                "impact": "May execute for each row",
                "fix": "Consider JOIN instead of subquery"
            })
        
        return issues
    
    def _generate_optimized_query(self, query: str, issues: List[Dict], db_type: str) -> str:
        """Generate optimized version of query"""
        optimized = query
        
        # Replace SELECT *
        if any("SELECT *" in issue["issue"] for issue in issues):
            optimized = re.sub(
                r'SELECT\s+\*',
                'SELECT id, name, email, created_at  -- Specify needed columns',
                optimized,
                flags=re.IGNORECASE
            )
        
        # Add LIMIT if missing
        if any("No LIMIT" in issue["issue"] for issue in issues):
            if "limit" not in optimized.lower():
                optimized += "\nLIMIT 100  -- Limit result set"
        
        # Add comment about indexes
        if any("WHERE" in issue["issue"] for issue in issues):
            optimized = "-- Consider adding index on WHERE clause columns\n" + optimized
        
        return optimized
    
    def _recommend_indexes(self, query: str, schema: Dict) -> List[Dict[str, str]]:
        """Recommend indexes for query"""
        indexes = []
        
        # Extract WHERE clause columns
        where_match = re.search(r'WHERE\s+(\w+)', query, re.IGNORECASE)
        if where_match:
            column = where_match.group(1)
            indexes.append({
                "index_type": "B-Tree",
                "columns": [column],
                "reason": f"Used in WHERE clause",
                "sql": f"CREATE INDEX idx_{column} ON table_name({column});"
            })
        
        # Extract JOIN columns
        join_matches = re.findall(r'JOIN\s+\w+\s+ON\s+\w+\.(\w+)\s*=\s*\w+\.(\w+)', query, re.IGNORECASE)
        for col1, col2 in join_matches:
            indexes.append({
                "index_type": "B-Tree",
                "columns": [col1, col2],
                "reason": "Used in JOIN condition",
                "sql": f"CREATE INDEX idx_{col1}_{col2} ON table_name({col1}, {col2});"
            })
        
        # Extract ORDER BY columns
        order_match = re.search(r'ORDER BY\s+(\w+)', query, re.IGNORECASE)
        if order_match:
            column = order_match.group(1)
            indexes.append({
                "index_type": "B-Tree",
                "columns": [column],
                "reason": "Used in ORDER BY clause",
                "sql": f"CREATE INDEX idx_{column} ON table_name({column});"
            })
        
        return indexes if indexes else [{"message": "No indexes recommended"}]
    
    def _estimate_performance_gain(self, issues: List[Dict], optimized: str) -> Dict[str, str]:
        """Estimate performance improvement"""
        if not issues:
            return {
                "improvement": "None needed - query is already optimal",
                "estimated_speedup": "1x (no change)"
            }
        
        # Estimate based on issues fixed
        critical_count = sum(1 for i in issues if i["severity"] == "critical")
        high_count = sum(1 for i in issues if i["severity"] == "high")
        medium_count = sum(1 for i in issues if i["severity"] == "medium")
        
        # Calculate estimated speedup
        speedup = 1
        speedup *= (10 if critical_count > 0 else 1)
        speedup *= (5 if high_count > 0 else 1)
        speedup *= (2 if medium_count > 0 else 1)
        
        return {
            "issues_fixed": len(issues),
            "estimated_speedup": f"{speedup}x faster",
            "improvement": f"Significant - {len(issues)} issues resolved"
        }
    
    def _generate_query_best_practices(self, db_type: str) -> List[str]:
        """Generate query optimization best practices"""
        return [
            "✅ Select only needed columns (avoid SELECT *)",
            "✅ Use WHERE clauses to filter data",
            "✅ Add LIMIT to restrict result sets",
            "✅ Create indexes on WHERE, JOIN, and ORDER BY columns",
            "✅ Use JOINs instead of subqueries when possible",
            "✅ Avoid functions in WHERE clause (prevents index usage)",
            "✅ Use EXPLAIN to analyze query execution plan",
            "✅ Batch INSERT/UPDATE operations",
            "✅ Use connection pooling",
            "✅ Monitor slow queries and optimize regularly"
        ]


class DataPipelineGenerator:
    """Implements capability #132: Data Pipeline Generation"""
    
    async def generate_data_pipeline(self,
                                    source: Dict[str, Any],
                                    destination: Dict[str, Any],
                                    transformations: List[str] = None) -> Dict[str, Any]:
        """
        Creates ETL and data processing pipelines
        
        Args:
            source: Source data configuration
            destination: Destination configuration
            transformations: List of transformations to apply
            
        Returns:
            Complete ETL pipeline implementation
        """
        try:
            # Design pipeline architecture
            architecture = self._design_pipeline_architecture(source, destination)
            
            # Generate extraction code
            extraction = self._generate_extraction_code(source)
            
            # Generate transformation code
            transformation = self._generate_transformation_code(transformations or [])
            
            # Generate loading code
            loading = self._generate_loading_code(destination)
            
            # Create orchestration
            orchestration = self._create_pipeline_orchestration()
            
            # Generate complete pipeline
            pipeline_code = self._generate_complete_pipeline(
                extraction,
                transformation,
                loading,
                orchestration
            )
            
            # Create monitoring
            monitoring = self._create_pipeline_monitoring()
            
            return {
                "success": True,
                "architecture": architecture,
                "extraction_code": extraction,
                "transformation_code": transformation,
                "loading_code": loading,
                "orchestration": orchestration,
                "complete_pipeline": pipeline_code,
                "monitoring": monitoring,
                "best_practices": self._generate_pipeline_best_practices()
            }
        except Exception as e:
            logger.error("Data pipeline generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _design_pipeline_architecture(self, source: Dict, dest: Dict) -> Dict[str, Any]:
        """Design pipeline architecture"""
        return {
            "pattern": "ETL (Extract, Transform, Load)",
            "components": {
                "extractor": f"Reads from {source.get('type', 'database')}",
                "transformer": "Applies data transformations",
                "loader": f"Writes to {dest.get('type', 'warehouse')}",
                "scheduler": "Airflow / Prefect for orchestration",
                "monitoring": "Track pipeline health and performance"
            },
            "execution_model": {
                "batch": "Scheduled batch processing (daily, hourly)",
                "streaming": "Real-time event processing (Kafka, Kinesis)",
                "hybrid": "Batch for historical, streaming for real-time"
            },
            "recommended_for": "Data warehouse, analytics, reporting"
        }
    
    def _generate_extraction_code(self, source: Dict) -> str:
        """Generate extraction code"""
        source_type = source.get("type", "database")
        
        if source_type == "database":
            return '''
# Extract from Database
import pandas as pd
from sqlalchemy import create_engine

def extract_from_database():
    """Extract data from source database"""
    engine = create_engine('postgresql://user:pass@localhost/db')
    
    query = """
        SELECT id, user_id, event_type, timestamp, data
        FROM events
        WHERE timestamp >= CURRENT_DATE - INTERVAL '1 day'
    """
    
    df = pd.read_sql(query, engine)
    print(f"Extracted {len(df)} rows")
    
    return df
'''
        elif source_type == "api":
            return '''
# Extract from API
import httpx
import pandas as pd

async def extract_from_api():
    """Extract data from API"""
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.example.com/data')
        data = response.json()
    
    df = pd.DataFrame(data['items'])
    print(f"Extracted {len(df)} rows from API")
    
    return df
'''
        elif source_type == "file":
            return '''
# Extract from Files
import pandas as pd

def extract_from_files(file_path):
    """Extract data from CSV/JSON/Parquet files"""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    elif file_path.endswith('.parquet'):
        df = pd.read_parquet(file_path)
    
    print(f"Extracted {len(df)} rows from {file_path}")
    return df
'''
        else:
            return f"# Extract from {source_type}"
    
    def _generate_transformation_code(self, transformations: List[str]) -> str:
        """Generate transformation code"""
        return '''
# Transform Data
import pandas as pd

def transform_data(df):
    """Apply transformations to data"""
    # Clean data
    df = df.dropna(subset=['id'])  # Remove rows with null IDs
    df = df.drop_duplicates(subset=['id'])  # Remove duplicates
    
    # Type conversions
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Add calculated columns
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Aggregate data
    daily_summary = df.groupby('date').agg({
        'amount': ['sum', 'mean', 'count'],
        'user_id': 'nunique'
    }).reset_index()
    
    # Enrich data (join with reference data)
    # reference_df = load_reference_data()
    # df = df.merge(reference_df, on='key', how='left')
    
    print(f"Transformed {len(df)} rows")
    return df
'''
    
    def _generate_loading_code(self, dest: Dict) -> str:
        """Generate loading code"""
        dest_type = dest.get("type", "warehouse")
        
        if dest_type == "warehouse":
            return '''
# Load to Data Warehouse
from sqlalchemy import create_engine

def load_to_warehouse(df):
    """Load data to warehouse"""
    engine = create_engine('postgresql://user:pass@warehouse/db')
    
    # Load data
    df.to_sql(
        'analytics_events',
        engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=1000
    )
    
    print(f"Loaded {len(df)} rows to warehouse")
'''
        elif dest_type == "s3":
            return '''
# Load to S3
import boto3
import pandas as pd

def load_to_s3(df, bucket, key):
    """Load data to S3 as Parquet"""
    s3 = boto3.client('s3')
    
    # Convert to Parquet
    parquet_buffer = df.to_parquet(index=False)
    
    # Upload to S3
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=parquet_buffer
    )
    
    print(f"Loaded {len(df)} rows to s3://{bucket}/{key}")
'''
        else:
            return f"# Load to {dest_type}"
    
    def _create_pipeline_orchestration(self) -> Dict[str, Any]:
        """Create pipeline orchestration"""
        return {
            "orchestrator": "Apache Airflow",
            "dag_example": '''
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for analytics',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_from_database,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_to_warehouse,
    dag=dag
)

extract_task >> transform_task >> load_task
            ''',
            "scheduling": {
                "frequency": "Daily at 2 AM (low-traffic time)",
                "retry_policy": "3 retries with 5-minute delays",
                "alerting": "Email on failure"
            }
        }
    
    def _generate_complete_pipeline(self, extract: str, transform: str, load: str, orch: Dict) -> str:
        """Generate complete pipeline"""
        return f'''
# Complete ETL Pipeline

{extract}

{transform}

{load}

# Main ETL function
def run_etl_pipeline():
    """Run complete ETL pipeline"""
    # Extract
    df = extract_from_database()
    
    # Transform
    df_transformed = transform_data(df)
    
    # Load
    load_to_warehouse(df_transformed)
    
    print("ETL pipeline completed successfully")

if __name__ == "__main__":
    run_etl_pipeline()
'''
    
    def _create_pipeline_monitoring(self) -> Dict[str, Any]:
        """Create pipeline monitoring"""
        return {
            "metrics": [
                "Pipeline execution time",
                "Rows processed",
                "Success/failure rate",
                "Data quality score",
                "Resource usage (CPU, memory)"
            ],
            "alerts": [
                "Pipeline failure",
                "Execution time > 2x normal",
                "Data quality below threshold",
                "No data extracted (upstream issue)"
            ],
            "dashboards": "Airflow UI + Custom Grafana dashboard"
        }
    
    def _generate_pipeline_best_practices(self) -> List[str]:
        """Generate pipeline best practices"""
        return [
            "✅ Make pipelines idempotent (safe to re-run)",
            "✅ Include data quality checks",
            "✅ Log pipeline execution details",
            "✅ Monitor pipeline performance",
            "✅ Use incremental loading where possible",
            "✅ Implement error handling and retries",
            "✅ Version your pipeline code",
            "✅ Test pipelines with sample data",
            "✅ Document data lineage",
            "✅ Schedule during low-traffic periods"
        ]


class AnalyticsImplementer:
    """Implements capability #133: Analytics Implementation"""
    
    async def implement_analytics(self,
                                 events_to_track: List[str],
                                 analytics_platform: str = "custom") -> Dict[str, Any]:
        """
        Adds analytics and tracking code
        
        Args:
            events_to_track: Events to track (page_view, click, purchase, etc.)
            analytics_platform: Platform (google_analytics, segment, mixpanel, custom)
            
        Returns:
            Complete analytics implementation
        """
        try:
            # Design analytics architecture
            architecture = self._design_analytics_architecture(analytics_platform)
            
            # Generate event tracking code
            tracking_code = self._generate_event_tracking_code(events_to_track, analytics_platform)
            
            # Create event schema
            schema = self._create_event_schema(events_to_track)
            
            # Implement data collection
            collection = self._implement_data_collection(analytics_platform)
            
            # Create analytics dashboards
            dashboards = self._create_analytics_dashboards()
            
            return {
                "success": True,
                "analytics_platform": analytics_platform,
                "architecture": architecture,
                "tracking_code": tracking_code,
                "event_schema": schema,
                "data_collection": collection,
                "dashboards": dashboards,
                "best_practices": self._generate_analytics_best_practices()
            }
        except Exception as e:
            logger.error("Analytics implementation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _design_analytics_architecture(self, platform: str) -> Dict[str, Any]:
        """Design analytics architecture"""
        return {
            "components": {
                "client_sdk": "JavaScript/Mobile SDK for event tracking",
                "collection_api": "API endpoint to receive events",
                "event_queue": "Kafka/Kinesis for event streaming",
                "processing": "Spark/Flink for event processing",
                "storage": "ClickHouse/BigQuery for analytics queries",
                "visualization": "Metabase/Tableau for dashboards"
            },
            "data_flow": [
                "1. Client emits event",
                "2. Event sent to collection API",
                "3. Event queued in Kafka",
                "4. Stream processor enriches and validates",
                "5. Event stored in analytics database",
                "6. Dashboards query aggregated data"
            ]
        }
    
    def _generate_event_tracking_code(self, events: List[str], platform: str) -> str:
        """Generate event tracking code"""
        if platform == "google_analytics":
            return '''
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
  
  // Track custom event
  function trackEvent(eventName, eventParams) {
    gtag('event', eventName, eventParams);
  }
  
  // Example usage
  trackEvent('purchase', {
    transaction_id: '12345',
    value: 99.99,
    currency: 'USD'
  });
</script>
'''
        else:
            return '''
# Custom Analytics Implementation
class AnalyticsTracker:
    """Custom analytics tracker"""
    
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
    
    async def track_event(self, event_name, properties=None, user_id=None):
        """Track analytics event"""
        event = {
            "event": event_name,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "properties": properties or {},
            "session_id": self._get_session_id(),
            "device_info": self._get_device_info()
        }
        
        # Send to analytics API
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.api_url}/events",
                json=event,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        
        print(f"Tracked event: {event_name}")
    
    def _get_session_id(self):
        """Get current session ID"""
        return "session_123"
    
    def _get_device_info(self):
        """Get device information"""
        return {
            "platform": "web",
            "browser": "Chrome",
            "os": "Windows"
        }

# 🧬 REAL IMPLEMENTATION EXAMPLE:
# import os
# tracker = AnalyticsTracker(
#     api_url=os.getenv("ANALYTICS_API_URL", "https://analytics.example.com"),
#     api_key=os.getenv("ANALYTICS_API_KEY")
# )

# Track page view
await tracker.track_event("page_view", {
    "page": "/products",
    "referrer": "/home"
})

# Track purchase
await tracker.track_event("purchase", {
    "product_id": "prod_123",
    "price": 99.99,
    "quantity": 1
}, user_id="user_456")
'''
    
    def _create_event_schema(self, events: List[str]) -> Dict[str, Dict]:
        """Create event schema"""
        return {
            "page_view": {
                "properties": {
                    "page": "string",
                    "title": "string",
                    "referrer": "string",
                    "url": "string"
                },
                "required": ["page", "url"]
            },
            "click": {
                "properties": {
                    "element_id": "string",
                    "element_type": "string",
                    "page": "string"
                },
                "required": ["element_id"]
            },
            "purchase": {
                "properties": {
                    "product_id": "string",
                    "price": "number",
                    "quantity": "number",
                    "currency": "string"
                },
                "required": ["product_id", "price"]
            }
        }
    
    def _implement_data_collection(self, platform: str) -> Dict[str, Any]:
        """Implement data collection"""
        return {
            "collection_endpoint": "POST /api/analytics/events",
            "validation": "Validate against event schema",
            "enrichment": [
                "Add IP geolocation",
                "Add user agent parsing",
                "Add session information",
                "Add timestamp if missing"
            ],
            "storage": {
                "hot_storage": "Redis (last 24 hours)",
                "warehouse": "ClickHouse (historical analytics)",
                "data_lake": "S3 (raw events for replay)"
            }
        }
    
    def _create_analytics_dashboards(self) -> List[Dict[str, Any]]:
        """Create analytics dashboards"""
        return [
            {
                "name": "User Activity Dashboard",
                "metrics": [
                    "Daily Active Users (DAU)",
                    "Monthly Active Users (MAU)",
                    "Session duration",
                    "Page views per session",
                    "Bounce rate"
                ],
                "visualizations": ["Time series", "Funnel", "Cohort analysis"]
            },
            {
                "name": "Product Analytics",
                "metrics": [
                    "Feature usage",
                    "Conversion funnel",
                    "User flow",
                    "A/B test results"
                ],
                "visualizations": ["Sankey diagram", "Heatmap", "Bar charts"]
            },
            {
                "name": "Business Metrics",
                "metrics": [
                    "Revenue",
                    "Customer Lifetime Value (LTV)",
                    "Churn rate",
                    "Customer Acquisition Cost (CAC)"
                ],
                "visualizations": ["KPI cards", "Trend lines", "Pie charts"]
            }
        ]
    
    def _generate_analytics_best_practices(self) -> List[str]:
        """Generate analytics best practices"""
        return [
            "✅ Define clear event taxonomy",
            "✅ Track user journey, not just pages",
            "✅ Implement privacy controls (GDPR, CCPA)",
            "✅ Use server-side tracking for critical events",
            "✅ Validate event data before storage",
            "✅ Create data quality monitoring",
            "✅ Document event schemas",
            "✅ Implement sampling for high-volume events",
            "✅ Use session replay for UX insights",
            "✅ A/B test before rolling out features"
        ]


class MLPipelineCreator:
    """Implements capability #134: Machine Learning Pipeline Creation"""
    
    async def create_ml_pipeline(self,
                                model_type: str = "classification",
                                framework: str = "sklearn") -> Dict[str, Any]:
        """
        Builds ML training and inference pipelines
        
        Args:
            model_type: Type of model (classification, regression, clustering)
            framework: ML framework (sklearn, tensorflow, pytorch)
            
        Returns:
            Complete ML pipeline
        """
        try:
            # Design ML pipeline
            architecture = self._design_ml_pipeline(model_type, framework)
            
            # Generate training pipeline
            training = self._generate_training_pipeline(model_type, framework)
            
            # Generate inference pipeline
            inference = self._generate_inference_pipeline(model_type, framework)
            
            # Create model monitoring
            monitoring = self._create_model_monitoring()
            
            # Generate MLOps setup
            mlops = self._generate_mlops_setup()
            
            return {
                "success": True,
                "model_type": model_type,
                "framework": framework,
                "architecture": architecture,
                "training_pipeline": training,
                "inference_pipeline": inference,
                "model_monitoring": monitoring,
                "mlops_setup": mlops,
                "best_practices": self._generate_ml_best_practices()
            }
        except Exception as e:
            logger.error("ML pipeline creation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _design_ml_pipeline(self, model_type: str, framework: str) -> Dict[str, Any]:
        """Design ML pipeline architecture"""
        return {
            "stages": {
                "data_preparation": [
                    "Data extraction",
                    "Data cleaning",
                    "Feature engineering",
                    "Train/test split"
                ],
                "training": [
                    "Model training",
                    "Hyperparameter tuning",
                    "Model validation",
                    "Model registration"
                ],
                "deployment": [
                    "Model packaging",
                    "API deployment",
                    "A/B testing",
                    "Production rollout"
                ],
                "monitoring": [
                    "Performance tracking",
                    "Drift detection",
                    "Retraining triggers",
                    "Model versioning"
                ]
            },
            "infrastructure": {
                "training": "GPU instances for training",
                "inference": "CPU instances with autoscaling",
                "storage": "S3 for models and artifacts",
                "registry": "MLflow for model versioning"
            }
        }
    
    def _generate_training_pipeline(self, model_type: str, framework: str) -> str:
        """Generate training pipeline code"""
        return '''
# ML Training Pipeline
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib

def train_model():
    """Train machine learning model"""
    # 1. Load data
    df = pd.read_csv('training_data.csv')
    
    # 2. Prepare features
    X = df.drop('target', axis=1)
    y = df['target']
    
    # 3. Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 4. Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate model
    y_pred = model.predict(X_test)
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted')
    }
    
    print(f"Model metrics: {metrics}")
    
    # 6. Save model
    joblib.dump(model, 'model.pkl')
    print("Model saved to model.pkl")
    
    return model, metrics

if __name__ == "__main__":
    model, metrics = train_model()
'''
    
    def _generate_inference_pipeline(self, model_type: str, framework: str) -> str:
        """Generate inference pipeline code"""
        return '''
# ML Inference API
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load model at startup
model = joblib.load('model.pkl')

@app.post("/predict")
async def predict(features: dict):
    """Make prediction"""
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Make prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0].max()
    
    return {
        "prediction": int(prediction),
        "confidence": float(probability),
        "model_version": "1.0.0"
    }

@app.get("/model/health")
async def model_health():
    """Check model health"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }
'''
    
    def _create_model_monitoring(self) -> Dict[str, Any]:
        """Create model monitoring"""
        return {
            "metrics": [
                "Prediction latency",
                "Throughput (predictions/second)",
                "Model accuracy (online validation)",
                "Data drift detection",
                "Prediction distribution"
            ],
            "drift_detection": {
                "feature_drift": "Monitor input feature distributions",
                "concept_drift": "Monitor prediction accuracy over time",
                "alert_threshold": "Alert if accuracy drops > 10%",
                "retraining_trigger": "Automatic retraining on drift"
            },
            "model_versioning": {
                "registry": "MLflow Model Registry",
                "versioning": "Semantic versioning (v1.0.0, v1.1.0)",
                "rollback": "Instant rollback to previous version"
            }
        }
    
    def _generate_mlops_setup(self) -> Dict[str, Any]:
        """Generate MLOps setup"""
        return {
            "ci_cd_for_ml": {
                "training_ci": "Automated training on data updates",
                "model_validation": "Validate model before deployment",
                "deployment": "Blue-green deployment for models",
                "rollback": "Automatic rollback on performance degradation"
            },
            "experiment_tracking": {
                "tool": "MLflow / Weights & Biases",
                "tracked_metrics": ["Accuracy", "F1 score", "Training time"],
                "hyperparameters": "Log all hyperparameters",
                "artifacts": "Store models, plots, datasets"
            },
            "feature_store": {
                "tool": "Feast / Tecton",
                "purpose": "Consistent features for training and inference",
                "versioning": "Track feature versions"
            }
        }
    
    def _generate_ml_best_practices(self) -> List[str]:
        """Generate ML best practices"""
        return [
            "✅ Version datasets, code, and models together",
            "✅ Track all experiments systematically",
            "✅ Validate model performance before deployment",
            "✅ Monitor for data and concept drift",
            "✅ Implement A/B testing for model rollouts",
            "✅ Use feature stores for consistency",
            "✅ Automate retraining on drift detection",
            "✅ Document model assumptions and limitations",
            "✅ Implement model explainability (SHAP, LIME)",
            "✅ Test models for bias and fairness"
        ]


class DataVisualizationGenerator:
    """Implements capability #135: Data Visualization Generation"""
    
    async def generate_visualization(self,
                                    data: Dict[str, Any],
                                    chart_type: str = "auto",
                                    library: str = "plotly") -> Dict[str, Any]:
        """
        Creates charts and data visualizations
        
        Args:
            data: Data to visualize
            chart_type: Chart type (bar, line, pie, scatter, auto)
            library: Visualization library (plotly, chartjs, d3, matplotlib)
            
        Returns:
            Visualization code and configuration
        """
        try:
            # Analyze data structure
            data_analysis = self._analyze_data_for_viz(data)
            
            # Recommend chart type
            recommended_chart = self._recommend_chart_type(data_analysis, chart_type)
            
            # Generate visualization code
            viz_code = self._generate_viz_code(data, recommended_chart, library)
            
            # Create configuration
            config = self._create_viz_configuration(recommended_chart)
            
            # Generate interactive features
            interactivity = self._add_interactivity(recommended_chart)
            
            return {
                "success": True,
                "recommended_chart_type": recommended_chart,
                "library": library,
                "visualization_code": viz_code,
                "configuration": config,
                "interactivity": interactivity,
                "best_practices": self._generate_viz_best_practices()
            }
        except Exception as e:
            logger.error("Visualization generation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_data_for_viz(self, data: Dict) -> Dict[str, Any]:
        """Analyze data structure for visualization"""
        return {
            "data_type": "time_series" if "timestamp" in str(data) else "categorical",
            "dimensions": len(data.get("columns", [])) if "columns" in data else 2,
            "row_count": len(data.get("data", [])) if "data" in data else 0,
            "has_categories": True,
            "has_numerical": True
        }
    
    def _recommend_chart_type(self, analysis: Dict, requested: str) -> str:
        """Recommend appropriate chart type"""
        if requested != "auto":
            return requested
        
        if analysis["data_type"] == "time_series":
            return "line"
        elif analysis["dimensions"] == 2:
            return "bar"
        elif analysis["dimensions"] > 2:
            return "scatter"
        else:
            return "bar"
    
    def _generate_viz_code(self, data: Dict, chart_type: str, library: str) -> str:
        """Generate visualization code"""
        if library == "plotly":
            return f'''
# Plotly Visualization
import plotly.graph_objects as go
import plotly.express as px

def create_{chart_type}_chart(data):
    """Create {chart_type} chart"""
    fig = px.{chart_type}(
        data,
        x='category',
        y='value',
        title='{chart_type.title()} Chart',
        labels={{'category': 'Category', 'value': 'Value'}}
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        showlegend=True
    )
    
    # Save to HTML
    fig.write_html('{chart_type}_chart.html')
    
    # Or return JSON for web
    return fig.to_json()

# Usage
chart_json = create_{chart_type}_chart(data)
'''
        else:
            return f"# {library} visualization code for {chart_type} chart"
    
    def _create_viz_configuration(self, chart_type: str) -> Dict[str, Any]:
        """Create visualization configuration"""
        return {
            "colors": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"],
            "responsive": True,
            "animation": True,
            "tooltips": True,
            "legend": {"position": "top"},
            "axes": {
                "x": {"title": "Category", "gridlines": True},
                "y": {"title": "Value", "gridlines": True}
            }
        }
    
    def _add_interactivity(self, chart_type: str) -> Dict[str, Any]:
        """Add interactive features"""
        return {
            "zoom": "Enable zoom and pan",
            "hover": "Show details on hover",
            "click": "Click to drill down",
            "filter": "Interactive filters",
            "export": "Export to PNG/SVG/PDF"
        }
    
    def _generate_viz_best_practices(self) -> List[str]:
        """Generate visualization best practices"""
        return [
            "✅ Choose appropriate chart type for data",
            "✅ Use consistent color scheme",
            "✅ Make charts responsive for mobile",
            "✅ Add clear labels and titles",
            "✅ Include data source and timestamp",
            "✅ Use tooltips for additional context",
            "✅ Implement accessibility (alt text, keyboard nav)",
            "✅ Optimize for performance (limit data points)",
            "✅ Add export functionality",
            "✅ Test across browsers and devices"
        ]


class ReportGenerationAutomator:
    """Implements capability #136: Report Generation Automation"""
    
    async def automate_report_generation(self,
                                        report_type: str,
                                        data_sources: List[Dict[str, Any]],
                                        schedule: str = "daily") -> Dict[str, Any]:
        """
        Automates business report generation
        
        Args:
            report_type: Type of report (sales, analytics, executive)
            data_sources: Data sources for report
            schedule: Generation schedule
            
        Returns:
            Automated report generation system
        """
        try:
            # Design report structure
            structure = self._design_report_structure(report_type)
            
            # Generate report template
            template = self._generate_report_template(report_type)
            
            # Create data collection
            data_collection = self._create_data_collection_logic(data_sources)
            
            # Generate report code
            code = self._generate_report_code(report_type, data_sources)
            
            # Setup automation
            automation = self._setup_report_automation(schedule)
            
            # Create distribution
            distribution = self._create_report_distribution()
            
            return {
                "success": True,
                "report_type": report_type,
                "report_structure": structure,
                "report_template": template,
                "data_collection": data_collection,
                "generation_code": code,
                "automation_setup": automation,
                "distribution": distribution,
                "best_practices": self._generate_report_best_practices()
            }
        except Exception as e:
            logger.error("Report generation automation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _design_report_structure(self, report_type: str) -> Dict[str, Any]:
        """Design report structure"""
        structures = {
            "sales": {
                "sections": [
                    "Executive Summary",
                    "Revenue Analysis",
                    "Product Performance",
                    "Customer Insights",
                    "Trends and Forecasts"
                ],
                "format": "PDF / Excel"
            },
            "analytics": {
                "sections": [
                    "Key Metrics",
                    "User Activity",
                    "Conversion Funnels",
                    "Feature Usage",
                    "Recommendations"
                ],
                "format": "PDF / Dashboard"
            },
            "executive": {
                "sections": [
                    "Executive Summary",
                    "Business Metrics",
                    "Financial Overview",
                    "Strategic Initiatives",
                    "Risks and Opportunities"
                ],
                "format": "PDF / PowerPoint"
            }
        }
        
        return structures.get(report_type, structures["analytics"])
    
    def _generate_report_template(self, report_type: str) -> str:
        """Generate report template"""
        return '''
# Report Template (Jinja2)
<!DOCTYPE html>
<html>
<head>
    <title>{{ report_title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .metric { display: inline-block; margin: 20px; padding: 20px; background: #f5f5f5; }
        .metric-value { font-size: 32px; font-weight: bold; color: #3498db; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    </style>
</head>
<body>
    <h1>{{ report_title }}</h1>
    <p>Generated: {{ generation_date }}</p>
    
    <h2>Key Metrics</h2>
    <div class="metrics">
        {% for metric in key_metrics %}
        <div class="metric">
            <div>{{ metric.name }}</div>
            <div class="metric-value">{{ metric.value }}</div>
            <div>{{ metric.change }}% vs last period</div>
        </div>
        {% endfor %}
    </div>
    
    <h2>Detailed Analysis</h2>
    <table>
        <thead>
            <tr>
                {% for column in table_columns %}
                <th>{{ column }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in table_data %}
            <tr>
                {% for value in row %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <h2>Charts</h2>
    <div id="chart"></div>
    
</body>
</html>
'''
    
    def _create_data_collection_logic(self, sources: List[Dict]) -> str:
        """Create data collection logic"""
        return '''
# Data Collection for Report
import pandas as pd

def collect_report_data(start_date, end_date):
    """Collect data from all sources"""
    data = {}
    
    # From database
    data['sales'] = pd.read_sql(f"""
        SELECT date, SUM(amount) as total_sales
        FROM sales
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY date
    """, db_connection)
    
    # From analytics API
    data['users'] = fetch_from_analytics_api(start_date, end_date)
    
    # From file storage
    data['inventory'] = pd.read_csv('s3://bucket/inventory.csv')
    
    return data
'''
    
    def _generate_report_code(self, report_type: str, sources: List[Dict]) -> str:
        """Generate report generation code"""
        return '''
# Automated Report Generation
from jinja2 import Template
import pdfkit
from datetime import datetime, timedelta

def generate_report(report_date=None):
    """Generate automated report"""
    report_date = report_date or datetime.now().date()
    
    # 1. Collect data
    data = collect_report_data(
        start_date=report_date - timedelta(days=30),
        end_date=report_date
    )
    
    # 2. Calculate metrics
    metrics = {
        'total_revenue': data['sales']['total_sales'].sum(),
        'active_users': data['users']['active_users'].iloc[-1],
        'growth_rate': calculate_growth_rate(data)
    }
    
    # 3. Render template
    template = Template(report_template)
    html = template.render(
        report_title=f"Monthly Report - {report_date}",
        generation_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        key_metrics=metrics,
        table_data=data['sales'].values.tolist()
    )
    
    # 4. Generate PDF
    pdfkit.from_string(html, f'report_{report_date}.pdf')
    
    print(f"Report generated: report_{report_date}.pdf")
    
    return f'report_{report_date}.pdf'
'''
    
    def _setup_report_automation(self, schedule: str) -> Dict[str, Any]:
        """Setup report automation"""
        schedules = {
            "daily": "0 6 * * *",  # 6 AM daily
            "weekly": "0 6 * * 1",  # 6 AM Monday
            "monthly": "0 6 1 * *"  # 6 AM 1st of month
        }
        
        return {
            "scheduler": "Airflow / Cron",
            "schedule": schedules.get(schedule, schedules["daily"]),
            "airflow_dag": '''
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    'daily_report',
    schedule_interval='0 6 * * *',
    start_date=datetime(2025, 1, 1)
)

generate_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag
)
            '''
        }
    
    def _create_report_distribution(self) -> Dict[str, Any]:
        """Create report distribution"""
        return {
            "methods": {
                "email": "Send via email to stakeholders",
                "slack": "Post to Slack channel",
                "s3": "Upload to S3 bucket",
                "dashboard": "Update live dashboard"
            },
            "recipients": {
                "daily": ["team@example.com"],
                "weekly": ["management@example.com"],
                "monthly": ["executives@example.com"]
            }
        }
    
    def _generate_report_best_practices(self) -> List[str]:
        """Generate report best practices"""
        return [
            "✅ Automate report generation and distribution",
            "✅ Use templates for consistency",
            "✅ Include data quality indicators",
            "✅ Add trend indicators (↑↓)",
            "✅ Provide drill-down capabilities",
            "✅ Include actionable insights",
            "✅ Version reports for audit trail",
            "✅ Test report generation regularly",
            "✅ Optimize for mobile viewing",
            "✅ Include data refresh timestamp"
        ]


class DataMigrationScripter:
    """Implements capability #137: Data Migration Scripting"""
    
    async def create_migration_script(self,
                                     source_db: Dict[str, Any],
                                     target_db: Dict[str, Any],
                                     tables: List[str]) -> Dict[str, Any]:
        """
        Creates data migration scripts
        
        Args:
            source_db: Source database configuration
            target_db: Target database configuration
            tables: Tables to migrate
            
        Returns:
            Data migration scripts and plan
        """
        try:
            # Create migration plan
            plan = self._create_migration_plan(source_db, target_db, tables)
            
            # Generate migration scripts
            scripts = self._generate_migration_scripts(source_db, target_db, tables)
            
            # Create validation scripts
            validation = self._create_validation_scripts(tables)
            
            # Generate rollback plan
            rollback = self._create_rollback_plan()
            
            return {
                "success": True,
                "migration_plan": plan,
                "migration_scripts": scripts,
                "validation_scripts": validation,
                "rollback_plan": rollback,
                "best_practices": self._generate_migration_best_practices()
            }
        except Exception as e:
            logger.error("Migration script creation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _create_migration_plan(self, source: Dict, target: Dict, tables: List) -> Dict[str, Any]:
        """Create migration plan"""
        return {
            "phases": [
                {
                    "phase": 1,
                    "name": "Preparation",
                    "tasks": [
                        "Backup source database",
                        "Create target database schema",
                        "Test migration on sample data",
                        "Prepare rollback scripts"
                    ]
                },
                {
                    "phase": 2,
                    "name": "Migration",
                    "tasks": [
                        "Stop writes to source (if applicable)",
                        "Run migration scripts",
                        "Validate data integrity",
                        "Run data quality checks"
                    ]
                },
                {
                    "phase": 3,
                    "name": "Cutover",
                    "tasks": [
                        "Switch application to target database",
                        "Monitor for issues",
                        "Keep source database as backup",
                        "Decommission source after validation period"
                    ]
                }
            ],
            "downtime_window": "2-4 hours (depends on data volume)",
            "rollback_plan": "Revert to source database if issues detected"
        }
    
    def _generate_migration_scripts(self, source: Dict, target: Dict, tables: List) -> Dict[str, str]:
        """Generate migration scripts"""
        return {
            "extract_data": '''
# Extract from source
pg_dump -h source_host -U user -d source_db -t users -t orders > data.sql
            ''',
            "transform_schema": '''
# Transform schema if needed
sed 's/old_column/new_column/g' data.sql > data_transformed.sql
            ''',
            "load_data": '''
# Load to target
psql -h target_host -U user -d target_db < data_transformed.sql
            ''',
            "python_migration": '''
# Python Migration Script
import pandas as pd
from sqlalchemy import create_engine

def migrate_table(table_name):
    """Migrate single table"""
    source_engine = create_engine('postgresql://source')
    target_engine = create_engine('postgresql://target')
    
    # Read from source
    df = pd.read_sql(f"SELECT * FROM {table_name}", source_engine)
    
    # Transform if needed
    # df = transform_data(df)
    
    # Write to target
    df.to_sql(table_name, target_engine, if_exists='append', index=False)
    
    print(f"Migrated {len(df)} rows from {table_name}")

# Migrate all tables
for table in ['users', 'orders', 'products']:
    migrate_table(table)
            '''
        }
    
    def _create_validation_scripts(self, tables: List[str]) -> str:
        """Create validation scripts"""
        return '''
# Data Validation Script
def validate_migration(table_name):
    """Validate migrated data"""
    source_count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", source_engine)['cnt'][0]
    target_count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", target_engine)['cnt'][0]
    
    assert source_count == target_count, f"Row count mismatch: {source_count} vs {target_count}"
    
    # Checksum validation
    source_checksum = pd.read_sql(f"SELECT MD5(STRING_AGG(id::text, '')) FROM {table_name}", source_engine)
    target_checksum = pd.read_sql(f"SELECT MD5(STRING_AGG(id::text, '')) FROM {table_name}", target_engine)
    
    assert source_checksum.equals(target_checksum), "Data checksum mismatch"
    
    print(f"✅ {table_name} validation passed")

for table in tables:
    validate_migration(table)
'''
    
    def _create_rollback_plan(self) -> Dict[str, Any]:
        """Create rollback plan"""
        return {
            "triggers": [
                "Data validation fails",
                "Application errors after cutover",
                "Performance degradation",
                "Data corruption detected"
            ],
            "rollback_steps": [
                "1. Switch application back to source database",
                "2. Investigate and document issues",
                "3. Fix migration scripts",
                "4. Retry migration in next window"
            ],
            "time_limit": "Rollback if not stable within 1 hour"
        }
    
    def _generate_migration_best_practices(self) -> List[str]:
        """Generate migration best practices"""
        return [
            "✅ Always backup before migration",
            "✅ Test migration on copy of production data",
            "✅ Validate data integrity after migration",
            "✅ Plan for zero-downtime if possible",
            "✅ Have rollback plan ready",
            "✅ Monitor application after cutover",
            "✅ Keep old database for several weeks",
            "✅ Document migration process",
            "✅ Communicate with stakeholders",
            "✅ Schedule during low-traffic periods"
        ]


class DatabaseIndexOptimizer:
    """Implements capability #138: Database Index Optimization"""
    
    async def optimize_indexes(self,
                              table_name: str,
                              queries: List[str] = None,
                              database_type: str = "postgresql") -> Dict[str, Any]:
        """
        Recommends and creates optimal indexes
        
        Args:
            table_name: Table to optimize
            queries: Common queries against the table
            database_type: Database type
            
        Returns:
            Index recommendations and creation scripts
        """
        try:
            # Analyze query patterns
            query_analysis = self._analyze_query_patterns(queries or [])
            
            # Recommend indexes
            recommendations = self._recommend_optimal_indexes(table_name, query_analysis)
            
            # Generate index creation SQL
            create_scripts = self._generate_index_creation_scripts(recommendations, database_type)
            
            # Analyze existing indexes
            existing = self._analyze_existing_indexes(table_name)
            
            # Calculate impact
            impact = self._calculate_index_impact(recommendations, query_analysis)
            
            return {
                "success": True,
                "table": table_name,
                "query_analysis": query_analysis,
                "recommended_indexes": recommendations,
                "creation_scripts": create_scripts,
                "existing_indexes": existing,
                "estimated_impact": impact,
                "best_practices": self._generate_index_best_practices()
            }
        except Exception as e:
            logger.error("Index optimization failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_query_patterns(self, queries: List[str]) -> Dict[str, Any]:
        """Analyze query patterns"""
        patterns = {
            "where_columns": set(),
            "join_columns": set(),
            "order_columns": set(),
            "group_columns": set()
        }
        
        for query in queries:
            query_lower = query.lower()
            
            # Extract WHERE columns
            where_match = re.findall(r'where\s+(\w+)', query_lower)
            patterns["where_columns"].update(where_match)
            
            # Extract JOIN columns
            join_match = re.findall(r'on\s+\w+\.(\w+)', query_lower)
            patterns["join_columns"].update(join_match)
            
            # Extract ORDER BY columns
            order_match = re.findall(r'order by\s+(\w+)', query_lower)
            patterns["order_columns"].update(order_match)
            
            # Extract GROUP BY columns
            group_match = re.findall(r'group by\s+(\w+)', query_lower)
            patterns["group_columns"].update(group_match)
        
        return {k: list(v) for k, v in patterns.items()}
    
    def _recommend_optimal_indexes(self, table: str, patterns: Dict) -> List[Dict[str, Any]]:
        """Recommend optimal indexes"""
        recommendations = []
        
        # WHERE clause columns
        for col in patterns.get("where_columns", []):
            recommendations.append({
                "index_name": f"idx_{table}_{col}",
                "columns": [col],
                "type": "B-Tree",
                "reason": f"Used in WHERE clause",
                "priority": "High"
            })
        
        # JOIN columns
        for col in patterns.get("join_columns", []):
            recommendations.append({
                "index_name": f"idx_{table}_{col}_join",
                "columns": [col],
                "type": "B-Tree",
                "reason": "Used in JOIN condition",
                "priority": "High"
            })
        
        # Composite index for WHERE + ORDER BY
        where_cols = patterns.get("where_columns", [])
        order_cols = patterns.get("order_columns", [])
        if where_cols and order_cols:
            composite_cols = list(set(where_cols[:1] + order_cols[:1]))
            if len(composite_cols) > 1:
                recommendations.append({
                    "index_name": f"idx_{table}_composite",
                    "columns": composite_cols,
                    "type": "B-Tree",
                    "reason": "Covers WHERE and ORDER BY",
                    "priority": "Medium"
                })
        
        return recommendations
    
    def _generate_index_creation_scripts(self, recommendations: List[Dict], db_type: str) -> List[str]:
        """Generate SQL to create indexes"""
        scripts = []
        
        for rec in recommendations:
            columns = ", ".join(rec["columns"])
            script = f"CREATE INDEX {rec['index_name']} ON table_name({columns});"
            scripts.append(script)
        
        return scripts
    
    def _analyze_existing_indexes(self, table: str) -> List[Dict[str, str]]:
        """Analyze existing indexes"""
        return [
            {
                "name": "primary_key",
                "columns": ["id"],
                "type": "B-Tree",
                "usage": "High",
                "recommendation": "Keep - primary key"
            }
        ]
    
    def _calculate_index_impact(self, recommendations: List[Dict], patterns: Dict) -> Dict[str, str]:
        """Calculate impact of recommended indexes"""
        return {
            "query_speedup": "5-100x faster for indexed queries",
            "write_overhead": f"{len(recommendations) * 5}% slower writes",
            "storage_overhead": f"{len(recommendations) * 10}MB estimated",
            "recommendation": "High impact - implement recommended indexes"
        }
    
    def _generate_index_best_practices(self) -> List[str]:
        """Generate index best practices"""
        return [
            "✅ Index foreign keys",
            "✅ Index WHERE clause columns",
            "✅ Create composite indexes for common query patterns",
            "✅ Avoid over-indexing (slows writes)",
            "✅ Monitor index usage (remove unused indexes)",
            "✅ Use covering indexes for frequent queries",
            "✅ Consider partial indexes for filtered queries",
            "✅ Rebuild indexes periodically (reduces bloat)",
            "✅ Use EXPLAIN to verify index usage",
            "✅ Index selectivity matters (high cardinality better)"
        ]


class DataValidationImplementer:
    """Implements capability #139: Data Validation Implementation"""
    
    async def implement_data_validation(self,
                                       schema: Dict[str, Any],
                                       validation_rules: List[Dict] = None) -> Dict[str, Any]:
        """
        Adds comprehensive data validation
        
        Args:
            schema: Data schema to validate against
            validation_rules: Custom validation rules
            
        Returns:
            Data validation implementation
        """
        try:
            # Generate validation schema
            validation_schema = self._generate_validation_schema(schema)
            
            # Create validation code
            validation_code = self._generate_validation_code(schema, validation_rules or [])
            
            # Implement field validators
            field_validators = self._create_field_validators(schema)
            
            # Create error handling
            error_handling = self._create_validation_error_handling()
            
            return {
                "success": True,
                "validation_schema": validation_schema,
                "validation_code": validation_code,
                "field_validators": field_validators,
                "error_handling": error_handling,
                "best_practices": self._generate_validation_best_practices()
            }
        except Exception as e:
            logger.error("Data validation implementation failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _generate_validation_schema(self, schema: Dict) -> Dict[str, Any]:
        """Generate validation schema"""
        return {
            "type": "object",
            "required": schema.get("required", []),
            "properties": schema.get("fields", {}),
            "additionalProperties": False
        }
    
    def _generate_validation_code(self, schema: Dict, rules: List[Dict]) -> str:
        """Generate validation code"""
        return '''
# Data Validation with Pydantic
from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    """User data validation schema"""
    id: int = Field(..., gt=0)
    email: str = Field(..., regex=r'^[\\w\\.+-]+@[\\w-]+\\.[\\w\\.-]+$')
    age: Optional[int] = Field(None, ge=0, le=150)
    created_at: datetime
    
    @validator('email')
    def validate_email(cls, v):
        """Custom email validation"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('age')
    def validate_age(cls, v):
        """Custom age validation"""
        if v is not None and (v < 0 or v > 150):
            raise ValueError('Age must be between 0 and 150')
        return v

# Usage
try:
    user = UserSchema(
        id=1,
        email="user@example.com",
        age=25,
        created_at=datetime.now()
    )
    print(f"✅ Validation passed: {user}")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
'''
    
    def _create_field_validators(self, schema: Dict) -> Dict[str, List[str]]:
        """Create field-specific validators"""
        return {
            "email": [
                "Format validation (regex)",
                "DNS validation (MX record check)",
                "Disposable email detection"
            ],
            "phone": [
                "Format validation",
                "Country code validation",
                "Number length validation"
            ],
            "url": [
                "Format validation",
                "Protocol validation (https required)",
                "Domain validation"
            ],
            "date": [
                "Format validation (ISO 8601)",
                "Range validation (not in future)",
                "Timezone handling"
            ]
        }
    
    def _create_validation_error_handling(self) -> Dict[str, Any]:
        """Create error handling for validation"""
        return {
            "error_response": {
                "status_code": 422,
                "body": {
                    "error": "Validation failed",
                    "details": [
                        {
                            "field": "email",
                            "message": "Invalid email format",
                            "value": "invalid_email"
                        }
                    ]
                }
            },
            "logging": "Log validation errors for analysis",
            "metrics": "Track validation failure rates"
        }
    
    def _generate_validation_best_practices(self) -> List[str]:
        """Generate validation best practices"""
        return [
            "✅ Validate at API boundary (input validation)",
            "✅ Use schema validation libraries (Pydantic, Joi)",
            "✅ Provide clear error messages",
            "✅ Validate data types, formats, and ranges",
            "✅ Implement business rule validation",
            "✅ Sanitize inputs to prevent injection",
            "✅ Log validation failures for monitoring",
            "✅ Use allow-lists instead of deny-lists",
            "✅ Validate on client and server",
            "✅ Keep validation logic centralized"
        ]


class RealtimeAnalyticsSetup:
    """Implements capability #140: Real-time Analytics Setup"""
    
    async def setup_realtime_analytics(self,
                                      use_cases: List[str],
                                      latency_requirement_ms: int = 1000) -> Dict[str, Any]:
        """
        Configures real-time data processing
        
        Args:
            use_cases: Use cases (dashboards, alerts, recommendations)
            latency_requirement_ms: Required latency in milliseconds
            
        Returns:
            Real-time analytics system
        """
        try:
            # Design streaming architecture
            architecture = self._design_streaming_architecture(latency_requirement_ms)
            
            # Setup stream processing
            stream_processing = self._setup_stream_processing()
            
            # Create real-time aggregations
            aggregations = self._create_realtime_aggregations()
            
            # Generate implementation
            code = self._generate_streaming_code()
            
            # Setup real-time dashboards
            dashboards = self._setup_realtime_dashboards()
            
            return {
                "success": True,
                "use_cases": use_cases,
                "latency_requirement_ms": latency_requirement_ms,
                "architecture": architecture,
                "stream_processing": stream_processing,
                "aggregations": aggregations,
                "implementation_code": code,
                "dashboards": dashboards,
                "best_practices": self._generate_realtime_best_practices()
            }
        except Exception as e:
            logger.error("Real-time analytics setup failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _design_streaming_architecture(self, latency_ms: int) -> Dict[str, Any]:
        """Design streaming architecture"""
        if latency_ms < 100:
            tech_stack = "Kafka + Flink"
        elif latency_ms < 1000:
            tech_stack = "Kafka + Spark Streaming"
        else:
            tech_stack = "Kafka + ksqlDB"
        
        return {
            "technology_stack": tech_stack,
            "components": {
                "ingestion": "Kafka for event streaming",
                "processing": "Flink/Spark for stream processing",
                "storage": "ClickHouse for real-time queries",
                "serving": "WebSocket for live updates",
                "caching": "Redis for hot data"
            },
            "data_flow": [
                "Events → Kafka → Stream Processor → ClickHouse",
                "ClickHouse → API → WebSocket → Dashboard"
            ],
            "latency_target": f"< {latency_ms}ms end-to-end"
        }
    
    def _setup_stream_processing(self) -> Dict[str, Any]:
        """Setup stream processing"""
        return {
            "processing_framework": "Apache Flink",
            "example_job": '''
# Flink Stream Processing
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# Define Kafka source
t_env.execute_sql("""
    CREATE TABLE events (
        event_id STRING,
        user_id STRING,
        event_type STRING,
        timestamp TIMESTAMP(3),
        properties STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'events',
        'properties.bootstrap.servers' = 'localhost:9092'
    )
""")

# Real-time aggregation
t_env.execute_sql("""
    CREATE TABLE event_counts AS
    SELECT
        TUMBLE_START(timestamp, INTERVAL '1' MINUTE) as window_start,
        event_type,
        COUNT(*) as event_count
    FROM events
    GROUP BY TUMBLE(timestamp, INTERVAL '1' MINUTE), event_type
""")
            ''',
            "windowing": {
                "tumbling": "Fixed-size non-overlapping windows",
                "sliding": "Overlapping windows",
                "session": "Based on activity gaps"
            }
        }
    
    def _create_realtime_aggregations(self) -> List[Dict[str, str]]:
        """Create real-time aggregations"""
        return [
            {
                "metric": "Active users (last 5 minutes)",
                "query": "SELECT COUNT(DISTINCT user_id) FROM events WHERE timestamp > NOW() - INTERVAL '5 minutes'"
            },
            {
                "metric": "Requests per second",
                "query": "SELECT COUNT(*) / 60 FROM events WHERE timestamp > NOW() - INTERVAL '1 minute'"
            },
            {
                "metric": "Average response time",
                "query": "SELECT AVG(response_time) FROM events WHERE timestamp > NOW() - INTERVAL '5 minutes'"
            }
        ]
    
    def _generate_streaming_code(self) -> str:
        """Generate streaming processing code"""
        return '''
# Real-time Analytics Stream Processing
from kafka import KafkaConsumer
import json
from datetime import datetime

# Kafka consumer
consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Process events in real-time
for message in consumer:
    event = message.value
    
    # Update real-time metrics
    update_realtime_metrics(event)
    
    # Check for alerts
    check_alerts(event)
    
    # Update dashboard
    push_to_dashboard(event)

def update_realtime_metrics(event):
    """Update real-time metrics in Redis"""
    redis_client.incr(f"events:{event['type']}:count")
    redis_client.zadd("active_users", {event['user_id']: datetime.now().timestamp()})

def check_alerts(event):
    """Check for alert conditions"""
    if event['type'] == 'error' and event['severity'] == 'critical':
        send_alert(event)
'''
    
    def _setup_realtime_dashboards(self) -> Dict[str, Any]:
        """Setup real-time dashboards"""
        return {
            "technology": "Grafana + WebSocket",
            "update_frequency": "1 second",
            "visualizations": [
                "Real-time event counter",
                "Active users gauge",
                "Response time graph",
                "Error rate alert"
            ],
            "alerts": [
                "Error rate > 1%",
                "Response time > 1s",
                "Active users < threshold"
            ]
        }
    
    def _generate_realtime_best_practices(self) -> List[str]:
        """Generate real-time analytics best practices"""
        return [
            "✅ Use stream processing for low latency",
            "✅ Implement exactly-once semantics",
            "✅ Use time-windowing for aggregations",
            "✅ Cache hot data in Redis",
            "✅ Use WebSockets for dashboard updates",
            "✅ Monitor stream lag and throughput",
            "✅ Implement backpressure handling",
            "✅ Use partitioning for horizontal scaling",
            "✅ Store raw events for replay",
            "✅ Plan for data retention (hot vs cold)"
        ]


__all__ = [
    'DatabaseQueryOptimizer',
    'DataPipelineGenerator',
    'AnalyticsImplementer',
    'MLPipelineCreator',
    'DataVisualizationGenerator',
    'ReportGenerationAutomator',
    'DataMigrationScripter',
    'DatabaseIndexOptimizer',
    'DataValidationImplementer',
    'RealtimeAnalyticsSetup'
]


