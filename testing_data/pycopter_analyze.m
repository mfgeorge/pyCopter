%% Script to plot testing data 
% Chad Bickel
% 12/11/16

clear all
close all
clc

filenames = {'pitch_log_p2high.csv','pitch_log_close2margstable.csv', ...
    'pitch_log_ponlytuned.csv','pitch_log_tunedWI.csv','pitch_log_Dadded.csv'};
titles = {'P=0.8, I=0, D=0','P=0.4, I=0, D=0','P=0.2, I=0, D=0','P=0.2, I=0.01, D=0',....
    'P=0.2, I=0.01, D = 0.05'};
figure(1)
for i = 1:length(filenames)
   filenames(i)
   A = csvread(char(filenames(i)));
   time_ms = A(:,1);
   pitch = A(:,2);
   %get rid of huge time values, not sure why these are appearing
   k = find((time_ms>1e8));
   time_ms(k) = NaN;
   k = find((time_ms<2.5e5));
   time_ms(k) = NaN;
   time_ms = (time_ms - min(time_ms))/1000;
   hold on 
   if i < 5
       subplot(2,2,i)
   else
       figure(i)
   end
   plot(time_ms,pitch); 
   xlabel('Time(s)')
   ylabel('Pitch(degrees)')
   title(char(titles(i)))
    
end