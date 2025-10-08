"""
Remove extracted classes from smart_coding_ai_optimized.py
"""

def remove_classes(source_file, class_names):
    """Remove classes from source file"""
    
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_until_next_class = False
    current_class = None
    
    for i, line in enumerate(lines):
        # Check if this is a class definition
        if line.startswith('class '):
            class_match = line.split('(')[0].split(':')[0].replace('class ', '').strip()
            
            if class_match in class_names:
                # Start skipping
                skip_until_next_class = True
                current_class = class_match
                # Add comment
                new_lines.append(f'# {class_match} extracted to smart_coding_ai_{class_match.lower().replace("service", "")}.py\n')
                new_lines.append('\n')
                continue
            else:
                # Stop skipping
                skip_until_next_class = False
                current_class = None
        
        # Skip lines if we're in a class to remove
        if skip_until_next_class:
            continue
        
        new_lines.append(line)
    
    # Write back
    with open(source_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Removed {len(class_names)} classes from {source_file}")

# Remove the infrastructure classes
remove_classes('app/services/smart_coding_ai_optimized.py', 
               ['QueueService', 'TelemetryService', 'OAuthService'])

print("Done!")

