"""
Batch Processing Example for Resume Analyzer

This example shows how to process multiple resumes in bulk.
"""

from resume_analyzer import analyze_resume
import os
import json
from datetime import datetime
import glob

def analyze_directory(directory_path, output_file='batch_results.json'):
    """
    Analyze all PDF resumes in a directory.
    
    Args:
        directory_path (str): Path to directory containing resume PDFs
        output_file (str): Path to save batch results
    """
    # Find all PDF files
    pdf_files = glob.glob(os.path.join(directory_path, '*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in {directory_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to analyze")
    print("="*60)
    
    results = []
    successful = 0
    failed = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_path)
        print(f"\n[{i}/{len(pdf_files)}] Analyzing: {filename}")
        
        try:
            result = analyze_resume(pdf_path)
            
            # Add metadata
            result['_metadata'] = {
                'filename': filename,
                'filepath': pdf_path,
                'analyzed_at': datetime.now().isoformat()
            }
            
            results.append(result)
            successful += 1
            
            # Print summary
            basic = result['basic_details']
            print(f"  ✓ Name: {basic.get('name', 'N/A')}")
            print(f"  ✓ Field: {result['predicted_field']}")
            print(f"  ✓ Score: {result['resume_score']}/100")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            failed += 1
            results.append({
                '_metadata': {
                    'filename': filename,
                    'filepath': pdf_path,
                    'analyzed_at': datetime.now().isoformat(),
                    'error': str(e)
                }
            })
    
    # Save results
    print("\n" + "="*60)
    print(f"Analysis complete: {successful} successful, {failed} failed")
    print(f"Saving results to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Done!")
    
    # Generate summary report
    generate_summary(results, f"{output_file.replace('.json', '_summary.txt')}")


def generate_summary(results, output_file):
    """Generate a text summary report."""
    
    with open(output_file, 'w') as f:
        f.write("BATCH RESUME ANALYSIS SUMMARY REPORT\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Resumes: {len(results)}\n\n")
        
        # Statistics
        successful = [r for r in results if '_metadata' in r and 'error' not in r['_metadata']]
        failed = [r for r in results if '_metadata' in r and 'error' in r['_metadata']]
        
        f.write(f"Successful Analyses: {len(successful)}\n")
        f.write(f"Failed Analyses: {len(failed)}\n\n")
        
        if successful:
            # Field distribution
            f.write("FIELD DISTRIBUTION:\n")
            f.write("-"*60 + "\n")
            fields = {}
            for r in successful:
                field = r.get('predicted_field', 'NA')
                fields[field] = fields.get(field, 0) + 1
            
            for field, count in sorted(fields.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {field}: {count}\n")
            
            # Experience level distribution
            f.write("\nEXPERIENCE LEVEL DISTRIBUTION:\n")
            f.write("-"*60 + "\n")
            levels = {}
            for r in successful:
                level = r.get('candidate_level', 'Unknown')
                levels[level] = levels.get(level, 0) + 1
            
            for level, count in sorted(levels.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {level}: {count}\n")
            
            # Score statistics
            scores = [r['resume_score'] for r in successful]
            if scores:
                f.write("\nSCORE STATISTICS:\n")
                f.write("-"*60 + "\n")
                f.write(f"  Average Score: {sum(scores)/len(scores):.1f}\n")
                f.write(f"  Highest Score: {max(scores)}\n")
                f.write(f"  Lowest Score: {min(scores)}\n")
            
            # Top candidates
            f.write("\nTOP 5 CANDIDATES (by score):\n")
            f.write("-"*60 + "\n")
            sorted_results = sorted(successful, key=lambda x: x['resume_score'], reverse=True)
            for i, r in enumerate(sorted_results[:5], 1):
                basic = r['basic_details']
                f.write(f"\n  {i}. {basic.get('name', 'N/A')}\n")
                f.write(f"     Score: {r['resume_score']}/100\n")
                f.write(f"     Field: {r['predicted_field']}\n")
                f.write(f"     Level: {r['candidate_level']}\n")
                f.write(f"     Email: {basic.get('email', 'N/A')}\n")
        
        if failed:
            f.write("\n\nFAILED ANALYSES:\n")
            f.write("-"*60 + "\n")
            for r in failed:
                meta = r['_metadata']
                f.write(f"\n  File: {meta['filename']}\n")
                f.write(f"  Error: {meta['error']}\n")
    
    print(f"Summary report saved to {output_file}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python batch_processing.py <directory_path> [output_file]")
        print("\nExample:")
        print("  python batch_processing.py ./resumes")
        print("  python batch_processing.py ./resumes results.json")
        sys.exit(1)
    
    directory = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'batch_results.json'
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)
    
    analyze_directory(directory, output_file)


if __name__ == '__main__':
    main()
