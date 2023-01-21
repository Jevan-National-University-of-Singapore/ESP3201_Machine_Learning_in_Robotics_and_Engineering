opts = detectImportOptions('MeasGT.csv');
opts.SelectedVariableNames = (2:3);
%measured_data = readmatrix('MeasGT.csv', opts);
x = 500;
y = -250;
Vx = 10; %random number for Vx Vy
Vy = 5;
Q0 = 0.1;
Vm = 12.5; %change later: max velocity
sigx = 10;
sigy = 10;

A = [1 0 1 0; 0 1 0 1; 0 0 1 0; 0 0 0 1];
X = [x; y; Vx; Vy]; %[x; y; Vx; Vy];
Z = readmatrix('MeasGT.csv', opts);%[MeasGT.mx MeasGT.my]; 
P = [sigx^2 0 0 0; 0 sigy^2 0 0; 0 0 Vm^2/9 0; 0 0 0 Vm^2/9];
R = [sigx^2 0; 0 sigy^2];
C = [1 0 0 0; 0 1 0 0];

Q = Q0 * [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];

%K: 4x2 Kalman Gain
%C: 2x4 transformation matrix with only 0 and 1
%R: 2x2 Measurement Noise [100 0; 0 100]
%wt: 4x1, white gaussian noise * X

% measured = [MeasGT.grdx MeasGT.grdy];
%MeasGT(5,2) %(row, column)
ansx = zeros(31,1);
ansy = zeros(31,1);
% truex = zeros(31,1);
% truey = zeros(31,1);
% meax = zeros(31,1);
% meay = zeros(31,1);
kalmangain = zeros(31,1);
for i = 1:31
    rngx = normrnd(0,0.1^2);
    rngy = normrnd(0, 0.1^2);
    rngvx = normrnd(0,0.1^2);
    rngvy =normrnd(0,0.1^2);
    noise = diag([rngx rngy rngvx rngvy]);
    Xp = A*X + noise*X; %next step
    P = A*P*transpose(A)+Q; %next step
    
    S = C*P*transpose(C) + R; %simplifying the matrix
    K = P*transpose(C)*pinv(S); %Kalman Gain
    
    IZ = [Z(i,1); Z(i,2)] - (C*Xp); %error term
    P = (eye(4) - K*C)*P;
    X = Xp + K*IZ; %update
    
    kalmangain(i) = IZ(1);
    
    ansx(i) = X(1,1);
    ansy(i) = X(2,1);
%     truex(i) = measured(i,1);
%     truey(i) = measured(i,2);
%     meax(i) = Z(i,1);
%     meay(i) = Z(i,2);
    
end
%plot(meax, meay);
%plot(ansx, ansy, 'k', truex, truey, 'r', meax, meay, 'c');
plot (ansx, ansy);




    
