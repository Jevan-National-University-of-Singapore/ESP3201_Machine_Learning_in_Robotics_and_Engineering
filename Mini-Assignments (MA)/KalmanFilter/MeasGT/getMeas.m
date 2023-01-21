function [measX, measY] = getMeas(iterations)
data = csvread('MeasGt.csv');
measX = data(1:iterations,2);
measY = data(1:iterations,3);

end