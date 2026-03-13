from fastapi import APIRouter

router = APIRouter()

@router.post("/generate-image")
async def generate_image(prompt: str, style: str = "su-embroidery"):
    """
    Generate image based on prompt and style using Stable Diffusion.
    """
    # Placeholder for SD generation logic
    return {
        "status": "success", 
        "image_url": "https://placeholder.com/generated-image.png",
        "prompt_used": prompt
    }

@router.post("/style-transfer")
async def style_transfer(image_data: str, target_style: str):
    """
    Apply craft style to user uploaded sketch/image.
    """
    return {"status": "success", "result_url": "https://placeholder.com/styled-image.png"}
