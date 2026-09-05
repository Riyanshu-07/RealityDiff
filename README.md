# RealityDiff

> AI-powered real-time scene change analyzer that detects what actually changed in a physical environment.

RealityDiff is a computer vision system designed to move beyond frame-by-frame object detection.

Instead of only asking:

**"What objects are visible right now?"**

RealityDiff asks:

**"What changed compared to the previous state?"**

It combines object detection, multi-object tracking, temporal state management, spatial reasoning, and persistent event storage to identify meaningful scene changes.

---

## The Problem

Traditional object detection works on individual frames.

For example:

```text
Frame 1 → Bottle detected
Frame 2 → Bottle detected
Frame 3 → Bottle detected
