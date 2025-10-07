import { SuperIntelligenceDashboard } from '@/components/super-intelligence/super-intelligence-dashboard'

export default function SuperIntelligencePage() {
  return (
    <div className="min-h-screen">
      <SuperIntelligenceDashboard
        enableAllFeatures={true}
        showAdvancedMetrics={true}
        enableRealTimeUpdates={true}
      />
    </div>
  )
}
