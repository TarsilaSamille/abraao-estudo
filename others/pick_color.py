#!/usr/bin/env python3
"""
Interactive and CLI color picker for images.
- Click anywhere on the image to get the exact sRGB hex.
- Averages a small NxN window around the click to reduce antialiasing noise.
- Copies the hex to the clipboard on macOS.
- Optional: compute a dominant color palette or average of a bounding box.

Usage:
    # Interactive (click to sample)
    python3 others/pick_color.py /path/to/image.png --window 5

    # CLI: average color of a bounding box (x0 y0 x1 y1)
    python3 others/pick_color.py /path/to/image.png --bbox 120 300 420 360

    # CLI: dominant palette (top N colors)
    python3 others/pick_color.py /path/to/image.png --palette 6

Press ESC or close the window to exit the interactive view.
"""
import argparse
import sys
import os
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def to_hex(r, g, b):
    r = int(np.clip(round(r), 0, 255))
    g = int(np.clip(round(g), 0, 255))
    b = int(np.clip(round(b), 0, 255))
    return f"#{r:02X}{g:02X}{b:02X}"


def contrast_text_color(r, g, b):
    # WCAG-like luma formula
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#111827" if brightness > 150 else "#ffffff"


def copy_to_clipboard(text):
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["pbcopy"], input=text, text=True, check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xclip", "-selection", "clipboard"], input=text, text=True, check=True)
        # On Windows, you can use 'clip' if needed, but not required here.
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Pick exact colors from an image by clicking or via CLI.")
    parser.add_argument("image", help="Path to image file")
    parser.add_argument("--window", type=int, default=3, help="Odd kernel size for local average (e.g., 3,5,7)")
    parser.add_argument("--bbox", nargs=4, type=int, metavar=("x0","y0","x1","y1"),
                        help="Compute average color in a bounding box without opening viewer")
    parser.add_argument("--palette", type=int, default=0, help="If >0, compute top-N dominant colors (k-means)")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    img = mpimg.imread(args.image)
    # Normalize to 0..255 if needed
    if img.dtype == np.float32 or img.dtype == np.float64:
        img = (img * 255).astype(np.uint8)

    if img.ndim == 2:
        img = np.stack([img, img, img], axis=-1)
    elif img.shape[2] == 4:
        # Drop alpha for calculation
        img = img[:, :, :3]

    win = max(1, args.window)
    if win % 2 == 0:
        win += 1

    # --- Non-interactive modes ---
    if args.bbox or args.palette:
        h, w = img.shape[:2]
        rgb = img[:, :, :3].reshape(-1, 3).astype(np.float32)

        def print_color(r, g, b, prefix=""):
            hex_color = to_hex(r, g, b)
            text_color = contrast_text_color(r, g, b)
            line = f"{prefix}{hex_color}\tRGB({int(r)},{int(g)},{int(b)})\ttexto={text_color}"
            print(line)
            copy_to_clipboard(hex_color)

        if args.bbox:
            x0, y0, x1, y1 = args.bbox
            x0 = int(np.clip(x0, 0, w-1))
            x1 = int(np.clip(x1, 0, w))
            y0 = int(np.clip(y0, 0, h-1))
            y1 = int(np.clip(y1, 0, h))
            if x1 <= x0 or y1 <= y0:
                print("Invalid bbox: ensure x1>x0 and y1>y0", file=sys.stderr)
                sys.exit(2)
            patch = img[y0:y1, x0:x1, :3].astype(np.float32)
            r, g, b = patch.reshape(-1, 3).mean(axis=0)
            print_color(r, g, b, prefix="bbox\t")
            # If bbox was provided without palette, exit early
            if not args.palette:
                return

        if args.palette and args.palette > 0:
            # Lightweight k-means on downsampled pixels for speed
            # Filter out near-white and near-black and very low saturation
            sample = rgb
            # Downsample to max 200k pixels to control memory
            max_pixels = 200_000
            if sample.shape[0] > max_pixels:
                idx = np.random.default_rng(42).choice(sample.shape[0], max_pixels, replace=False)
                sample = sample[idx]
            # Remove near-white/near-black
            brightness = sample.mean(axis=1)
            sat = sample.max(axis=1) - sample.min(axis=1)
            mask = (brightness > 25) & (brightness < 240) & (sat > 8)
            sample = sample[mask]
            if sample.size == 0:
                sample = rgb

            k = max(1, int(args.palette))
            # Initialize centroids randomly
            rng = np.random.default_rng(0)
            centroids = sample[rng.choice(sample.shape[0], k, replace=False)]
            for _ in range(10):  # a few iterations are enough
                # Assign
                dists = ((sample[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
                labels = dists.argmin(axis=1)
                # Update
                for i in range(k):
                    pts = sample[labels == i]
                    if pts.size:
                        centroids[i] = pts.mean(axis=0)
            # Count and sort by frequency
            dists = ((sample[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
            labels = dists.argmin(axis=1)
            counts = np.array([(labels == i).sum() for i in range(k)], dtype=int)
            order = counts.argsort()[::-1]
            total = counts.sum()
            for i in order:
                r, g, b = centroids[i]
                pct = counts[i] * 100.0 / total
                print_color(r, g, b, prefix=f"palette({pct:.1f}%)\t")
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img)
    ax.set_title("Clique para pegar a cor (hex será copiado)")
    ax.axis("off")

    text_anno = ax.text(0.02, 0.98, "", transform=ax.transAxes,
                        fontsize=12, color="#0ea5e9", va="top",
                        bbox=dict(boxstyle="round", fc="white", ec="#cbd5e1", alpha=0.9))

    def onclick(event):
        if event.inaxes != ax:
            return
        x = int(round(event.xdata))
        y = int(round(event.ydata))
        h, w, _ = img.shape
        half = win // 2
        x0, x1 = np.clip([x - half, x + half + 1], 0, w)
        y0, y1 = np.clip([y - half, y + half + 1], 0, h)
        patch = img[y0:y1, x0:x1, :]
        r, g, b = patch.reshape(-1, 3).mean(axis=0)
        hex_color = to_hex(r, g, b)
        text_color = contrast_text_color(r, g, b)
        copy_to_clipboard(hex_color)

        # Visual feedback
        ax.plot([x], [y], marker="o", markersize=8, markerfacecolor=hex_color, markeredgecolor="#111827")
        text_anno.set_text(f"{hex_color}\nRGB({int(r)}, {int(g)}, {int(b)})\nTexto: {text_color}")
        text_anno.set_color("#0ea5e9")
        fig.canvas.draw_idle()

        # Print to stdout as well
        print(hex_color)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    def onkey(event):
        if event.key == 'escape':
            plt.close(fig)
    fig.canvas.mpl_connect('key_press_event', onkey)

    plt.show()


if __name__ == "__main__":
    main()
