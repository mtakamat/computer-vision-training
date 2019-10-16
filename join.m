clear all;

pngfiles=dir('./*.png');
numfiles=length(pngfiles);
mydata=cell(1,numfiles);
for k=1:numfiles
    imgfullpath = fullfile(pngfiles(k).folder, pngfiles(k).name)
    IMG = imread(imgfullpath);
    w = size(IMG,2);
    h = size(IMG,1);
    mydata{k}=imcrop(IMG,[fix((w-h)/2),1,h,h]);

    mydata{k} = imresize(mydata{k},[256 256]);
    mydata{k}(:,:,1) = imadjust(mydata{k}(:,:,1));
    mydata{k}(:,:,2) = imadjust(mydata{k}(:,:,2));
    mydata{k}(:,:,3) = imadjust(mydata{k}(:,:,3));
    %imagesc(mydata{k}); colorbar; axis image;
     FileName = strcat(int2str(k), '.png')
    imwrite(mydata{k},FileName);
end


pngfiles=dir('./*.png');
numfiles=length(pngfiles);
mydata0=cell(1,numfiles);
for k=1:numfiles    
    IMG = imread(fullfile(pngfiles(k).folder, pngfiles(k).name));
    w = size(IMG,2);
    h = size(IMG,1);
    mydata0{k}=imcrop(IMG,[fix((w-h)/2),1,h,h]);
    mydata0{k} = imresize(mydata0{k},[256 256]);
    mydata0{k}(:,:,1) = imadjust(mydata0{k}(:,:,1));
    mydata0{k}(:,:,2) = imadjust(mydata0{k}(:,:,2));
    mydata0{k}(:,:,3) = imadjust(mydata0{k}(:,:,3));

    mydata{k} = [mydata0{k} mydata{k}];

    FileName = strcat( int2str(k), '.png')
    imwrite(mydata{k},FileName);
end