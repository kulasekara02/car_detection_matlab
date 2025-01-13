% Car Detection Algorithm using Image Processing Techniques

% Main detection function
function detectCar()
    % Read the input image with specific file path
    img = imread('C:\Users\VIHANGAK\Documents\dasun\15.png');
    
    % Convert to grayscale if image is RGB
    if size(img, 3) == 3
        gray = rgb2gray(img);
    else
        gray = img;
    end
    
    % Apply Gaussian blur to reduce noise
    blurred = imgaussfilt(gray, 2);
    
    % Edge detection using Canny
    edges = edge(blurred, 'canny', [0.1 0.3]);
    
    % Morphological operations to connect edges
    se = strel('disk', 2);
    dilated = imdilate(edges, se);
    
    % Fill holes in the image
    filled = imfill(dilated, 'holes');
    
    % Remove small objects
    cleaned = bwareaopen(filled, 1000);
    
    % Find connected components
    [labeled, numObjects] = bwlabel(cleaned);
    stats = regionprops(labeled, 'Area', 'BoundingBox');
    
    % Display results
    figure('Name', 'Car Detection Results');
    
    % Original image
    subplot(2,2,1);
    imshow(img);
    title('Original Image');
    
    % Edge detection result
    subplot(2,2,2);
    imshow(edges);
    title('Edge Detection');
    
    % Processed image
    subplot(2,2,3);
    imshow(cleaned);
    title('Processed Image');
    
    % Final result with bounding box
    subplot(2,2,4);
    imshow(img);
    hold on;
    
    % Draw bounding boxes around detected objects
    for i = 1:numObjects
        if stats(i).Area > 5000  % Filter by area to avoid small detections
            bbox = stats(i).BoundingBox;
            rectangle('Position', bbox, 'EdgeColor', 'r', 'LineWidth', 2);
        end
    end
    title('Car Detection Result');
    hold off;
end

% Function to evaluate detection performance
function [precision, recall] = evaluateDetection(groundTruth, detected)
    intersection = groundTruth & detected;
    precision = sum(intersection(:)) / sum(detected(:));
    recall = sum(intersection(:)) / sum(groundTruth(:));
end