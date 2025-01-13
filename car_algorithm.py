% Read the input image
img = imread('C:\Users\VIHANGAK\Documents\dasun\16.png');

% Convert to grayscale
gray = rgb2gray(img);

% Try multiple threshold sensitivities
sensitivities = [0.3, 0.4, 0.5, 0.6];
success = false;

for sensitivity = sensitivities
    % Create mask using current sensitivity
    mask = imbinarize(gray, 'adaptive', 'Sensitivity', sensitivity);
    
    % Get image dimensions
    [rows, cols] = size(gray);
    
    % Create center ROI (making it larger)
    centerROI = false(size(mask));
    centerROI(round(rows*0.2):round(rows*0.8), round(cols*0.2):round(cols*0.8)) = true;
    mask = mask & centerROI;
    
    % Clean up mask
    se = strel('disk', 5);
    mask = imclose(mask, se);
    mask = imfill(mask, 'holes');
    
    % Try different area thresholds
    for minArea = [1000, 2000, 3000, 4000, 5000]
        cleanMask = bwareaopen(mask, minArea);
        cc = bwconncomp(cleanMask);
        
        if cc.NumObjects > 0
            % Get the largest object
            stats = regionprops(cc, 'Area');
            [~, idx] = max([stats.Area]);
            carMask = false(size(mask));
            carMask(cc.PixelIdxList{idx}) = true;
            
            success = true;
            break;
        end
    end
    
    if success
        break;
    end
end

if ~success
    error('Could not detect car. Please check the image path and content.');
end

% Create yellow highlight
yellow = cat(3, ones(size(gray))*255, ones(size(gray))*255, zeros(size(gray)));

% Create highlighted image
highlighted = img;
mask3D = repmat(carMask, [1 1 3]);
highlighted(mask3D) = uint8(0.3 * yellow(mask3D) + 0.7 * double(img(mask3D)));

% Display result
figure;
imshow(highlighted);
title('Car Detection');

% Add bounding box
stats = regionprops(carMask, 'BoundingBox');
hold on;
rectangle('Position', stats.BoundingBox, 'EdgeColor', 'y', 'LineWidth', 2);
hold off;