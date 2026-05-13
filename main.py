import os
import glob
import pandas as pd
from tqdm import tqdm
import config
from extractors.azure_extractor import AzureExtractor
from extractors.gemini_extractor import GeminiExtractor

def main():
    print("Initializing Extractors...")
    azure_extractor = None
    gemini_extractor = None
    
    try:
        azure_extractor = AzureExtractor()
        print("✅ Azure Document Intelligence initialized.")
    except Exception as e:
        print(f"⚠️ Azure Initialization Warning: {e}")

    try:
        gemini_extractor = GeminiExtractor()
        print("✅ Gemini 1.5 Flash initialized.")
    except Exception as e:
        print(f"⚠️ Gemini Initialization Warning: {e}")

    if not azure_extractor and not gemini_extractor:
        print("❌ Both extractors failed to initialize. Please check your .env credentials.")
        return

    image_dir = config.IMAGE_DIR
    if not os.path.exists(image_dir):
        print(f"❌ Image directory '{image_dir}' not found.")
        print("Please create the folder, add the Kaggle dataset images to it, and update .env if necessary.")
        return

    # Gather image paths
    image_paths = glob.glob(os.path.join(image_dir, "*.jpg")) + \
                  glob.glob(os.path.join(image_dir, "*.png")) + \
                  glob.glob(os.path.join(image_dir, "*.jpeg"))
                  
    if not image_paths:
        print(f"❌ No images found in {image_dir}")
        return

    print(f"\nFound {len(image_paths)} images. Starting extraction pipeline...\n")

    all_results = []
    
    # Required keys for consistent ordering
    keys = [
        "Seller Name", "Seller Tax ID", "Client Name", "Client Tax ID",
        "Invoice Number", "Invoice Date", "Net Worth", "VAT", "Gross Worth"
    ]

    for img_path in tqdm(image_paths, desc="Processing Invoices"):
        filename = os.path.basename(img_path)
        
        # Pipeline A: Azure Document Intelligence
        if azure_extractor:
            azure_res = azure_extractor.extract(img_path)
            azure_res["Filename"] = filename
            azure_res["Pipeline"] = "Azure Document Intelligence"
            all_results.append(azure_res)
        
        # Pipeline B: Gemini 1.5 Flash Multimodal
        if gemini_extractor:
            gemini_res = gemini_extractor.extract(img_path)
            gemini_res["Filename"] = filename
            gemini_res["Pipeline"] = "Gemini 1.5 Flash"
            all_results.append(gemini_res)

    # Save outputs to CSV
    df = pd.DataFrame(all_results)
    
    if df.empty:
        print("No results extracted.")
        return

    # Reorder columns
    cols = ["Filename", "Pipeline"] + keys
    df = df[cols]
    
    df.to_csv(config.OUTPUT_FILE, index=False)
    print(f"\n✅ Saved extraction results to {config.OUTPUT_FILE}")

    # Generate Comparison Report if both pipelines were active
    if azure_extractor and gemini_extractor:
        print("Generating Comparison Report...")
        comparison_data = []
        
        for filename, group in df.groupby("Filename"):
            if len(group) == 2:
                azure_row = group[group["Pipeline"] == "Azure Document Intelligence"].iloc[0]
                gemini_row = group[group["Pipeline"] == "Gemini 1.5 Flash"].iloc[0]
                
                comp_row = {"Filename": filename}
                match_count = 0
                
                for key in keys:
                    val_a = str(azure_row[key]).strip().lower() if pd.notna(azure_row[key]) and azure_row[key] else "none"
                    val_b = str(gemini_row[key]).strip().lower() if pd.notna(gemini_row[key]) and gemini_row[key] else "none"
                    
                    is_match = (val_a == val_b)
                    # If both are none, we don't count it as a positive match for accuracy sake, 
                    # but if you prefer, you can count it. Let's count matching valid extractions.
                    if is_match and val_a != "none":
                        match_count += 1
                        
                    comp_row[f"{key} (Azure)"] = azure_row[key]
                    comp_row[f"{key} (Gemini)"] = gemini_row[key]
                    comp_row[f"{key} Match"] = is_match

                comp_row["Total Valid Matches"] = match_count
                comp_row["Match Rate (%)"] = round((match_count / len(keys)) * 100, 2)
                comparison_data.append(comp_row)

        if comparison_data:
            comp_df = pd.DataFrame(comparison_data)
            comp_df.to_csv(config.COMPARISON_FILE, index=False)
            print(f"✅ Saved comparison report to {config.COMPARISON_FILE}")
            
            avg_match = comp_df["Match Rate (%)"].mean()
            print(f"\n📊 Summary: Average Match Rate between Pipeline A and Pipeline B: {avg_match:.2f}%")
        else:
            print("Could not generate comparison. Not enough overlapping data.")

if __name__ == "__main__":
    main()
