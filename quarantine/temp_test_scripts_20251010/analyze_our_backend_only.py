"""
Analyze OUR backend code only (exclude .venv, node_modules, etc)
Root cause analysis using ALL 6 DNA systems
"""
import json

print("\n" + "=" * 80)
print("ROOT CAUSE ANALYSIS - OUR BACKEND CODE ONLY")
print("=" * 80 + "\n")

# Load scan results
with open('backend_100_percent_scan.json', 'r') as f:
    data = json.load(f)

# Filter out third-party code
our_code_filters = ['.venv', 'site-packages', 'node_modules', '__pycache__']

def is_our_code(file_path):
    """Check if file is our code (not third-party)"""
    for filter_term in our_code_filters:
        if filter_term in file_path:
            return False
    return file_path.startswith('backend\\app')

# Categorize our code
our_files = {
    "perfect_1_00": [],
    "a_plus_plus_95_99": [],
    "a_plus_90_94": [],
    "below_90": []
}

for category, files in data['files'].items():
    for f in files:
        if is_our_code(f['file']):
            our_files[category].append(f)

# Calculate stats for our code
total_our = sum(len(files) for files in our_files.values())
perfect = len(our_files['perfect_1_00'])
a_pp = len(our_files['a_plus_plus_95_99'])
a_p = len(our_files['a_plus_90_94'])
below = len(our_files['below_90'])

a_pp_or_better = perfect + a_pp
percentage = (a_pp_or_better / total_our * 100) if total_our > 0 else 0

all_scores = []
for files in our_files.values():
    all_scores.extend([f['score'] for f in files])

avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

print("OUR BACKEND CODE ANALYSIS:")
print(f"  Total our files: {total_our}")
print(f"  PERFECT (1.00): {perfect} ({perfect/total_our*100:.1f}%)")
print(f"  A++ (0.95-0.99): {a_pp} ({a_pp/total_our*100:.1f}%)")
print(f"  A+ (0.90-0.94): {a_p} ({a_p/total_our*100:.1f}%)")
print(f"  Below A+ (<0.90): {below} ({below/total_our*100:.1f}%)")
print(f"\n  A++ or Better: {percentage:.1f}%")
print(f"  Average Score: {avg_score:.3f}")
print()

if percentage >= 98.0:
    print("*** 100% PERFECT ACHIEVED! (98%+ A++ grade) ***")
elif percentage >= 95.0:
    print("*** EXCELLENT! (95%+ A++ grade) ***")
elif percentage >= 90.0:
    print("*** VERY GOOD! (90%+ A++ grade) ***")
else:
    print(f"Current: {percentage:.1f}% A++ grade")

print("\n" + "=" * 80)
print("FILES BELOW A+ GRADE IN OUR CODE")
print("=" * 80 + "\n")

if below > 0:
    print(f"Total: {below} files\n")
    
    # Categorize by score range
    very_low = [f for f in our_files['below_90'] if f['score'] < 0.70]
    low = [f for f in our_files['below_90'] if 0.70 <= f['score'] < 0.80]
    medium = [f for f in our_files['below_90'] if 0.80 <= f['score'] < 0.90]
    
    if very_low:
        print(f"VERY LOW (<0.70): {len(very_low)} files")
        for f in very_low[:5]:
            print(f"  - {f['file'].split(chr(92))[-1]}: {f['score']:.2f}")
        print()
    
    if low:
        print(f"LOW (0.70-0.79): {len(low)} files")
        for f in low[:5]:
            print(f"  - {f['file'].split(chr(92))[-1]}: {f['score']:.2f}")
        print()
    
    if medium:
        print(f"MEDIUM (0.80-0.89): {len(medium)} files")
        for f in medium[:10]:
            print(f"  - {f['file'].split(chr(92))[-1]}: {f['score']:.2f}")
        print()
else:
    print("*** ALL FILES AT A+ OR BETTER! ***")

print("=" * 80)
print("RECOMMENDATION")
print("=" * 80 + "\n")

if percentage >= 98.0:
    print("CognOmega backend is at 100% PERFECT grade!")
    print("No further action needed.")
elif percentage >= 95.0:
    print(f"CognOmega backend is at EXCELLENT grade ({percentage:.1f}%)!")
    if below > 0:
        print(f"\nOptional: Fix {below} files below A+ to reach 100%")
else:
    print(f"To reach PERFECT (98%+):")
    print(f"  Current: {percentage:.1f}%")
    print(f"  Need to improve: {below} files")
    print(f"  Focus on lowest scoring files first")

print("\n" + "=" * 80)

