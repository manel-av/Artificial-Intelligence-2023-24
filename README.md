# Artificial Intelligence - Image Labeling and Pathfinding Projects
## About This Course
This hands-on AI course covered fundamental algorithms through two major projects: optimal pathfinding in metro networks and automated image labeling for fashion items. The course progressively built from basic to advanced implementations, emphasizing both theoretical understanding and practical application.

## Practical Work
### Project 1: Metro Navigation System (Weeks 1-6)
#### Part 1: Uninformed Search (Weeks 1-2)
- Implemented depth-first and breadth-first search algorithms
- Developed core path expansion and cycle removal functions
- Built a subway map representation system with station connections
Key challenge: Managing path storage in reverse order (root-first) while maintaining algorithm correctness.

#### Part 2: Informed Search (Weeks 3-4)
- Created uniform cost search with multiple optimization criteria:
  - Number of stops
  - Travel time
  - Distance
  - Transfers
- Implemented A* algorithm with heuristic functions for each criterion
- Added redundant path elimination for optimization

### Advanced Features (Weeks 5-6)
- Developed coordinate-based navigation (A*_improved)
- Implemented walking transitions between arbitrary points and stations
- Created hybrid routes combining walking and metro travel

### Project 2: Fashion Image Labeling (Weeks 7-12)
#### Part 1: Color Labeling with K-Means (Weeks 7-8)
- Built K-Means clustering for dominant color extraction
- Implemented multiple centroid initialization methods:
  - First distinct points
  - Random selection
  - Last distinct points
- Automated optimal K selection using WCD thresholding
- Mapped RGB centroids to 11 basic color labels

#### Part 2: Shape Classification with KNN (Weeks 9-10)
- Developed K-Nearest Neighbors classifier for 8 clothing categories
- Implemented efficient distance calculations using vectorization
- Created voting system for neighbor-based classification
- Processed grayscale image features (80×60 pixels → 4800 dimensions)

#### Part 3: System Integration and Improvements (Weeks 11-12)
- Combined color and shape classifiers into unified labeling system
- Implemented quality metrics:
  - Color accuracy (compared to ground truth)
  - Shape classification accuracy
  - Retrieval performance analysis
- Added advanced features:
  - Multiple distance metrics for KNN
  - Improved K-Means initialization
  - Combined color-shape retrieval

## Final Thoughts
From implementing basic search algorithms to building a complete image labeling system, this course provided comprehensive AI implementation experience. The progressive structure - moving from foundational algorithms to integrated systems - made complex concepts manageable while demonstrating real-world AI applications.

Special thanks to my teammates for their collaboration on these challenging projects. The hands-on approach transformed theoretical knowledge into practical skills I can apply to future AI challenges.
