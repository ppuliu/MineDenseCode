function A=getAdjacentM(file_name,N)

t=load(file_name);
A=zeros(N,N);
for i=1:length(t)
    A(t(i,1),t(i,2))=1;
end

