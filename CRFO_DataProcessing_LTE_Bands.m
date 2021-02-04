% Author: Prabhu Chandhar, Chandhar Research Labs, Chennai, India.
% https://chandhar-labs.com

clc;
%clear all;

SamplingRate = 19.2e6; 
filename = 'CRF_LTE_Band40-2340_18-03-2019.bin';


fid = fopen(filename, 'r');
x = fread(fid, inf, 'int8');
fclose(fid);

x = (x(1:2:end) + 1i.*x(2:2:end))./128;
x = x - mean(x); % remove DC



%%%%%%%%%%%%% Plotting Time Domain Samples %%%%%%%%%%%%%%

rbw = 50e3;

x1 = x(1 : (50e-3*SamplingRate));
x1 = x1(:).';

figure;
plot((0:(length(x1)-1))./SamplingRate/1e-3, real(x1));
xlabel('Time (ms)');ylabel('Amplitude');hold on;
plot((0:(length(x1)-1))./SamplingRate/1e-3, imag(x1), 'r'); grid on;
legend('Real(x)','Imag(x)');


%%%%%%%%%%%%% Plotting Frequency Spectrum %%%%%%%%%%%%%%
spec = abs(fft(x1)).^2;
% spec = [spec((end/2)+1 : end) spec(1:(end/2))];
spec = fftshift(spec);
end_time = length(x1)/SamplingRate;
spec = filter_wo_tail(spec.', ones(1, floor(rbw*end_time)+1), 1);

figure; plot( [(1e-6.*(0:(length(x1)-1))./end_time ) - (1e-6*SamplingRate/2)]+2340, 10.*log10(spec)); grid on;
xlabel('Frequency (MHz)');ylabel('Power (dB)');hold on;


%%%%%%%%%%%%% Plotting PDF of received signal power %%%%%%%%%%%%%%
z = abs(x(1:60000));
figure;[u] = histogram(z,'normalization', 'pdf');hold on;
xlabel('Received signal amplitude');ylabel('PDF');hold on;

scale_param = raylfit(z);
r = 0:.01:max(z);
p = raylpdf(r,scale_param);plot(r,p,'r','LineWidth',2);
legend('PDF from measurement samples','Theory');
