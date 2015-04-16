function writeClusterFile(cidx,file_name)
clusterN=max(cidx);
fileID = fopen(file_name,'w');

for i=1:clusterN
    t=find(cidx==i);
    for j=1:length(t)
        fprintf(fileID,'%d\t',t(j)-1);
    end
    fprintf(fileID,'\n');
end
fclose(fileID);

