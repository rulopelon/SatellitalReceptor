clc, clear ,close all 
%% Code to generate a random qpsk signal to test on the reciever
random_vector = randi(2,1000,1);
random_vector = random_vector-1;

qpskmod = comm.QPSKModulator("SymbolMapping","Binary");
% Modulating the signal
signal = qpskmod(random_vector);

fid = fopen('qpsdkReal.txt','wt');
for ii = 1:size(signal,1)
    fprintf(fid,'%g\t',real(signal(ii,:)));
    fprintf(fid,'\n');
end
fclose(fid)

fid = fopen('qpsdkImag.txt','wt');
for ii = 1:size(signal,1)
    fprintf(fid,'%g\t',imag(signal(ii,:)));
    fprintf(fid,'\n');
end
fclose(fid)

fid = fopen('reference.txt','wt');
for ii = 1:size(random_vector,1)
    fprintf(fid,'%g\t',random_vector(ii,:));
    fprintf(fid,'\n');
end
fclose(fid)