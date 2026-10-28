"""Looping MP4 background playback for the Pygame viewer."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any


class VideoBackground:
    """Decode a video into Pygame surfaces using a local FFmpeg binary."""

    def __init__(
        self, pygame: Any, path: Path, size: tuple[int, int]
    ) -> None:
        self._pygame = pygame
        self._path = path
        self._width, self._height = size
        self._frame_size = self._width * self._height * 3
        self._process: Any = None
        self._frame: Any = None
        self._warned = False

    def start(self) -> None:
        """Start looping playback, keeping the caller's fallback available."""

        executable = self._find_ffmpeg()
        if executable is None:
            self._warn_once(
                "FFmpeg was not found; using the static background instead."
            )
            return

        filter_spec = (
            f"scale={self._width}:{self._height}:"
            "force_original_aspect_ratio=increase,"
            f"crop={self._width}:{self._height}"
        )
        command = [
            executable,
            "-loglevel",
            "error",
            "-re",
            "-stream_loop",
            "-1",
            "-i",
            str(self._path),
            "-an",
            "-vf",
            filter_spec,
            "-pix_fmt",
            "rgb24",
            "-f",
            "rawvideo",
            "pipe:1",
        ]

        try:
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                bufsize=self._frame_size,
            )
        except OSError:
            self._warn_once(
                "The video background could not be started; "
                "using the static background instead."
            )

    def draw(self, screen: Any) -> bool:
        """Draw the next frame and report whether video playback is active."""

        if self._process is not None and self._process.stdout is not None:
            frame = self._process.stdout.read(self._frame_size)
            if len(frame) == self._frame_size:
                self._frame = self._pygame.image.frombuffer(
                    frame, (self._width, self._height), "RGB"
                ).convert()
            else:
                self._frame = None
                self.stop()

        if self._frame is not None:
            screen.blit(self._frame, (0, 0))
            return True
        return False

    def stop(self) -> None:
        """Stop the decoder process and release its pipe."""

        if self._process is None:
            return
        process = self._process
        self._process = None
        process.terminate()
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        finally:
            if process.stdout is not None:
                process.stdout.close()

    def _find_ffmpeg(self) -> str | None:
        executable = shutil.which("ffmpeg")
        if executable is not None:
            return executable

        try:
            import imageio_ffmpeg

            return str(imageio_ffmpeg.get_ffmpeg_exe())
        except (ImportError, RuntimeError):
            return None

    def _warn_once(self, message: str) -> None:
        if not self._warned:
            print(message)
            self._warned = True
