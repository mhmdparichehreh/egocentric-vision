import json
import uuid
import random

def filter_data():
    #Removes queries which start time is later in the video than its end time, might have come from errors in the narration file.
    with open("augmented_nlq0.json", 'r') as f:
            data = json.load(f)

    samples = []

    for item in data:
        if item["clip_start_sec"] < item["clip_end_sec"]:
            samples.append(item)

    print(len(samples))

    #Create .json file
    with open("augmented_nlq1.json", "w") as f:
        json.dump(samples, f, indent=2)
        

    print(len(samples))
    


def generate_sample_json(queries, output_path="augmented_nlq.json"):
    #Generates a .json file of the same format as the original NLQ data from Ego4D, 
    # using our created .json file that had a simpler format.
    dataset = {"videos": []}

    for video_index in range(len(queries)):
        video_uid = queries[video_index]["video_uid"]
        video = {
            "video_uid": video_uid,
            "clips": []
        }

        # Each video has 1 clip
        for clip_index in range(1):
            clip_uid = video_uid
            video_start_sec = max(0, queries[video_index]["clip_start_sec"] - 60)
            video_end_sec = queries[video_index]["clip_end_sec"] + 60
            clip_start_sec = max(0, video_start_sec + 30)
            clip_end_sec = video_end_sec - 30
            video_start_frame = int(video_start_sec * 30)
            video_end_frame = int(video_end_sec * 30)
            clip_start_frame = int(clip_start_sec * 30)
            clip_end_frame = int(clip_end_sec * 30)

            annotations = []

            for ann_index in range(1):
                annotation_uid = str(uuid.uuid4())
                query = queries[video_index]["query"]

                # One language query per annotation
                language_queries = [{
                    "clip_start_sec": queries[video_index]["clip_start_sec"],
                    "clip_end_sec": queries[video_index]["clip_end_sec"],
                    "video_start_sec": queries[video_index]["clip_start_sec"],
                    "video_end_sec": queries[video_index]["clip_end_sec"],
                    "video_start_frame": int(queries[video_index]["clip_start_sec"] * 30),
                    "video_end_frame": int(queries[video_index]["clip_end_sec"] * 30),
                    "query": query
                }]

                annotation = {
                    "annotation_uid": annotation_uid,
                    "language_queries": language_queries
                }

                annotations.append(annotation)

            clip = {
                "clip_uid": clip_uid,
                "video_start_sec": video_start_sec,
                "video_end_sec": video_end_sec,
                "video_start_frame": video_start_frame,
                "video_end_frame": video_end_frame,
                "clip_start_sec": clip_start_sec,
                "clip_end_sec": clip_end_sec,
                "clip_start_frame": clip_start_frame,
                "clip_end_frame": clip_end_frame,
                "source_clip_uid": clip_uid,
                "annotations": annotations
            }

            video["clips"].append(clip)

        dataset["videos"].append(video)

    # Save to JSON
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"Saved dataset to {output_path}")

with open("augmented_nlq2.json", 'r') as f:
    data = json.load(f)
generate_sample_json(data)