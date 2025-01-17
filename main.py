% Read the input image
img = imread('C:\Users\VIHANGAK\Documents\dasun\15.png');

% Convert to grayscale if image is RGB
if size(img, 3) == 3
    gray = rgb2gray(img);
else
    gray = img;
end

% Apply Gaussian blur to reduce noise
blurred = imgaussfilt(gray, 2);

% Edge detection with optimized parameters for car detection
edges = edge(blurred, 'canny', [0.1 0.2]);

% Create mask for car region
se = strel('disk', 3);
dilated = imdilate(edges, se);
filled = imfill(dilated, 'holes');
cleaned = bwareaopen(filled, 1000);

% Create highlighted car image
highlighted = img;
mask = repmat(cleaned, [1 1 3]);  % Create 3D mask for RGB
highlighted(~mask) = 0;  % Make background black

% Display original and highlighted result
figure;
subplot(1,2,1), imshow(img), title('Original Image');
subplot(1,2,2), imshow(highlighted), title('Highlighted Car');

% Optional: Save the highlighted car image
% imwrite(highlighted, 'highlighted_car.png');