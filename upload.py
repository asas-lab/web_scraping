import argparse
from huggingface_hub import hf_api
from datasets import load_dataset

def push_dataset_to_hub(dataset_path, hf_repository_name, hf_token):

    # Load the dataset
    dataset = load_dataset('json', data_files=dataset_path)

    # Push to hub
    dataset.push_to_hub(hf_repository_name, token=hf_token)
    print(f"Dataset pushed successfully to: {hf_repository_name}")

def main():
    parser = argparse.ArgumentParser(description="Push a dataset to Hugging Face Hub.")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the dataset file.")
    parser.add_argument("--hf_repository_name", type=str, required=True, help="Hugging Face repository name.")
    parser.add_argument("--hf_token", type=str, required=True, help="Hugging Face API token.")
    args = parser.parse_args()

    push_dataset_to_hub(args.dataset_path, args.hf_repository_name, args.hf_token)

if __name__ == "__main__":
    main()
