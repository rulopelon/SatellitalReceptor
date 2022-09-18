%QPSK signal generation by sid
close all;
clear all;
clc;
msg=round(rand(1,20));
data=[];
t=0:.01:.99;
c=cos(2*pi*10*t);%carrier signal & it's a matrix of length 1X100(bcoz for each t, there's a c).let fc=10hz
for i=1:20
    if msg(i)==0
        d=-1*ones(1,10);
    else
        d=ones(1,10);
    end;
 data=[data d];   %data is created only for plotting.it has no application in the following for loop
end;
disp('length of t,c,data');
a=[length(t);length(c);length(data);];disp(a);
qpsk=[];
for i=1:2:20
    if msg(i)==1 && msg(i+1)== 0
        qpsk=[qpsk cos(2*pi*10*t+(pi/4))];
    else if msg(i)==0 && msg(i+1)==0
        qpsk=[qpsk cos(2*pi*10*t+(3*pi/4))];
        else if msg(i)==0 && msg(i+1)==1 
        qpsk=[qpsk cos(2*pi*10*t+(5*pi/4))];
            else if msg(i)==1 && msg(i+1)==1
        qpsk=[qpsk cos(2*pi*10*t+(7*pi/4))];
                end;
            end;
        end;
    end;
end;
%plot(qpsk);
modsig=[];
for i=1:100:1000
    for j=1:10
        p=qpsk(i+j);
        modsig=[modsig p]; 
    end;
end;
subplot(311);
plot(data);axis([0 100 -1.5 1.5])
title('Digital Message signal');
subplot(313);
plot(modsig);axis([0 100 -1.5 1.5])
title('QPSK signal');
subplot(312)
plot(c);axis([0 100 -1.5 1.5])
title('Unmodulated carrier');
