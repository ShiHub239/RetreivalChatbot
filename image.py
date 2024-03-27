import base64
import requests
import os
import io
from dotenv import load_dotenv
from langchain.agents import tool
from PIL import Image

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv()

# os.environ['STABILITY_KEY'] = 

stability_api = client.StabilityInference(
    key=os.environ.get("DIFFUSION_KEY"),
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0"
)




@tool
def generate_image(prompt):
    """ Generate an image based on the given prompt. 
        You must elaborate and expand upon the prompt to ensure that the user's specifications are met as accurately as possible.
        Try and describe the criteria you've used for that image.
        The resulting image should be found in the pictures folder.

        Returns True if the generation was a success

        Args:
            prompt: The given prompt describing the desired image
    """


    pics = stability_api.generate(
        prompt=prompt,
        seed=4253978046
    )


    for resp in pics:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save("./pictures/"+ str(artifact.seed)+ ".png")
            else:
                return False

    return True
    
