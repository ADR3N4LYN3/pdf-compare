"""
PDF Differ module - Detects and highlights differences between images
"""

from PIL import Image, ImageChops, ImageDraw, ImageFilter
from typing import Tuple, List, Optional
import numpy as np


class BoundingBox:
    """Represents a bounding box around a difference region"""

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def area(self) -> int:
        return self.width * self.height

    def __repr__(self) -> str:
        return f"BoundingBox(x={self.x1}, y={self.y1}, w={self.width}, h={self.height})"


class PDFDiffer:
    """Handles pixel-level comparison and difference detection"""

    def __init__(self, threshold: int = 0):
        """
        Initialize the differ

        Args:
            threshold: Pixel difference threshold (0-255). Pixels with difference
                      below this threshold are considered identical. Default: 0 (exact match)
        """
        self.threshold = threshold

    def compare_images(self, img1: Image.Image, img2: Image.Image) -> Tuple[bool, Image.Image, int]:
        """
        Compare two images and generate a diff image

        Args:
            img1: First image
            img2: Second image

        Returns:
            Tuple of (are_identical, diff_image, diff_pixel_count)
            - are_identical: True if images are identical within threshold
            - diff_image: Image highlighting differences in red
            - diff_pixel_count: Number of pixels that differ
        """
        # Ensure images have the same size
        if img1.size != img2.size:
            raise ValueError("Images must have the same dimensions for comparison")

        # Convert to RGB if needed
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        if img2.mode != 'RGB':
            img2 = img2.convert('RGB')

        # Calculate absolute difference
        diff = ImageChops.difference(img1, img2)

        # Convert to grayscale for easier threshold detection
        diff_gray = diff.convert('L')

        # Apply threshold
        if self.threshold > 0:
            diff_array = np.array(diff_gray)
            diff_array[diff_array <= self.threshold] = 0
            diff_gray = Image.fromarray(diff_array, mode='L')

        # Count different pixels
        diff_pixels = np.count_nonzero(np.array(diff_gray))

        # Create highlighted diff image (red overlay on original)
        diff_highlighted = img1.copy()

        # Create a red mask for differences
        diff_mask = diff_gray.point(lambda x: 255 if x > 0 else 0)
        red_overlay = Image.new('RGB', img1.size, (255, 0, 0))

        # Blend the red overlay where there are differences
        diff_highlighted.paste(red_overlay, mask=diff_mask)

        are_identical = bool(diff_pixels == 0)

        return are_identical, diff_highlighted, diff_pixels

    def find_difference_regions(self, img1: Image.Image, img2: Image.Image) -> List[BoundingBox]:
        """
        Find bounding boxes around contiguous regions of differences

        Args:
            img1: First image
            img2: Second image

        Returns:
            List of BoundingBox objects representing difference regions
        """
        # Get the difference
        diff = ImageChops.difference(img1.convert('RGB'), img2.convert('RGB'))
        diff_gray = diff.convert('L')

        # Apply threshold
        if self.threshold > 0:
            diff_array = np.array(diff_gray)
            diff_array[diff_array <= self.threshold] = 0
            diff_gray = Image.fromarray(diff_array, mode='L')

        # Convert to binary (differences are white)
        threshold_value = 1
        diff_binary = diff_gray.point(lambda x: 255 if x >= threshold_value else 0)

        # Find bounding boxes using connected components
        # This is a simplified approach - for production, consider using OpenCV
        bboxes = self._find_bounding_boxes(diff_binary)

        return bboxes

    def _find_bounding_boxes(self, binary_image: Image.Image) -> List[BoundingBox]:
        """
        Find bounding boxes in a binary image using a flood-fill approach

        Args:
            binary_image: Binary image with white (255) for differences

        Returns:
            List of BoundingBox objects
        """
        arr = np.array(binary_image)
        visited = np.zeros_like(arr, dtype=bool)
        bboxes = []

        height, width = arr.shape

        def flood_fill(start_x: int, start_y: int) -> Optional[BoundingBox]:
            """Flood fill to find connected component bounds"""
            if arr[start_y, start_x] == 0 or visited[start_y, start_x]:
                return None

            stack = [(start_x, start_y)]
            min_x, min_y = start_x, start_y
            max_x, max_y = start_x, start_y

            while stack:
                x, y = stack.pop()

                if x < 0 or x >= width or y < 0 or y >= height:
                    continue
                if visited[y, x] or arr[y, x] == 0:
                    continue

                visited[y, x] = True
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

                # Add neighbors
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

            return BoundingBox(min_x, min_y, max_x + 1, max_y + 1)

        # Scan for unvisited white pixels
        for y in range(height):
            for x in range(width):
                if arr[y, x] > 0 and not visited[y, x]:
                    bbox = flood_fill(x, y)
                    if bbox and bbox.area > 10:  # Ignore very small regions (noise)
                        bboxes.append(bbox)

        return bboxes

    def create_annotated_diff(self, img1: Image.Image, img2: Image.Image,
                             highlight_color: Tuple[int, int, int] = (255, 0, 0),
                             box_regions: bool = True) -> Image.Image:
        """
        Create an annotated difference image with colored overlays and optional bounding boxes

        Args:
            img1: First image
            img2: Second image
            highlight_color: RGB color for highlighting differences (default: red)
            box_regions: If True, draw bounding boxes around difference regions

        Returns:
            Annotated difference image
        """
        # Get basic diff
        _, diff_img, _ = self.compare_images(img1, img2)

        if box_regions:
            # Find regions and draw bounding boxes
            regions = self.find_difference_regions(img1, img2)
            draw = ImageDraw.Draw(diff_img)

            for bbox in regions:
                # Draw rectangle around difference region
                draw.rectangle(
                    [bbox.x1, bbox.y1, bbox.x2, bbox.y2],
                    outline=highlight_color,
                    width=3
                )

        return diff_img

    def calculate_similarity_percentage(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Calculate the percentage of similarity between two images

        Args:
            img1: First image
            img2: Second image

        Returns:
            Similarity percentage (0.0 to 100.0)
        """
        _, _, diff_pixels = self.compare_images(img1, img2)
        total_pixels = img1.width * img1.height * 3  # RGB channels

        similarity = ((total_pixels - diff_pixels) / total_pixels) * 100
        return similarity
