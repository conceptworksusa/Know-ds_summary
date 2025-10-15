import pandas as pd
import logging
from typing import Dict, List

class TaskGenerator:
    def __init__(self, logger_name="TaskGenerator"):
        # Initialize logger only
        self.logger = logging.getLogger(logger_name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.logger.info("Logger initialized successfully.")

    def load_csv(self, csv_path: str) -> pd.DataFrame:
        """Load input CSV file"""
        try:
            df = pd.read_csv(csv_path)
            self.logger.info(f"CSV loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            raise

    def process_controls(self, df: pd.DataFrame, domain_summary_map: Dict[str, str]) -> pd.DataFrame:
        """
        Process each domain and control.
        For each control, check if summary contains related information.
        (LLM logic can be added later)
        """
        output_records = []

        for _, row in df.iterrows():
            domain = row.get("dDomain", "").strip()
            controls_raw = row.get("Controls", "")
            
            if pd.isna(domain) or pd.isna(controls_raw):
                continue

            controls = [c.strip() for c in str(controls_raw).split(",") if c.strip()]
            summary_text = domain_summary_map.get(domain, "")

            self.logger.info(f"Processing domain: {domain} ({len(controls)} controls)")

            for control in controls:
                # Placeholder — Replace this with LLM-based check later
                is_present = self.simple_check(summary_text, control)
                output_records.append({
                    "Domain": domain,
                    "Control": control,
                    "FoundInSummary": is_present
                })

        result_df = pd.DataFrame(output_records)
        self.logger.info(f"Processed {len(result_df)} control entries.")
        return result_df

    def simple_check(self, summary: str, control: str) -> bool:
        """Basic text check (case-insensitive) — placeholder for LLM"""
        return control.lower() in summary.lower()

    def save_to_csv(self, df: pd.DataFrame, output_path: str):
        """Save results to CSV"""
        try:
            df.to_csv(output_path, index=False)
            self.logger.info(f"Results saved successfully to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")
            raise


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    generator = TaskGenerator()

    csv_file = "input.csv"
    domain_summary = {
        "Generative AI": "The assessment confirms that generative AI usage in processing Amex data is addressed...",
        "Data Privacy": "Controls are in place for managing user data securely..."
    }

    df = generator.load_csv(csv_file)
    result = generator.process_controls(df, domain_summary)
    generator.save_to_csv(result, "output.csv")
