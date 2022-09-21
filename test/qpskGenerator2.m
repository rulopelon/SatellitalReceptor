%% Data generation
N=15*10^5; % Amount of data
Qpsk=[1+1i ­1i ­1+1i ­­1i]; % Four possible complex No. for QPSK
data= Qpsk(randi(4,1,N)); % The data
Tsym=100; % No.of samples per symbol
noise=(randn(1,length(data)*Tsym)+1i*randn(1,length(data)*Tsym));
%Generating random numbers for n1
%% pulse shape
p = sin(2*pi*(0:Tsym­1)/(2*Tsym));%Sinusoidal wave
data_up = zeros(1,length(data)*Tsym);%Creation a memory of zeros
data_up(1:Tsym:end) = data; %Interpolation the data

S11 = conv(data_up,p); %The convolution operation
S1=S11(1:end­99); %Remove last 99 bits that are added due to the convolution