#!/usr/bin/env python3
from src.cluster_status import show_cluster_status_progress

def infra__cluster_status():
    try: 
        show_cluster_status_progress()
    except Exception as e:
        print(f"An error occurred:")
        print(e)
        print(e.output)

if __name__ == "__main__":
    infra__cluster_status()