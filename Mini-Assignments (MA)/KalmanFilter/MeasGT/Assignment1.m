
%*****************************************************************
%                       Kalman Filter Code
%*****************************************************************

%======================== import of data ============================
opts = detectImportOptions('MeasGT.csv');
opts.SelectedVariableNames = (2:5);
measured_data = readmatrix('MeasGT.csv', opts);

%---------- measured vales ----------------
measured_x = measured_data(1:31,1);
measured_y = measured_data(1:31,2);

% ----------- Ground truths ---------------
groundT_x = measured_data(1:31,3);
groundT_y = measured_data(1:31,4);

%===================== end of import ==============================

% --------------- initialising of variables -----------------------
x = 500;      % initial predicted x
y = -200;   % initial predicted y
v_x = 10;   % initial predicted x velocity
v_y = 10;    % initial predicted y velocity
v_max = 12.5;   % estimate of maximum velocity for an initial covariance matrix prediction
Q0 = 0.01;   % small process noise variance
std_measured_x = 10;    % standard deviation for measured x values
std_measured_y = 10;    % standard deviation for measured y values

X = [x; y; v_x; v_y];   % state matrix
A = [1 0 1 0; 0 1 0 1; 0 0 1 0; 0 0 0 1]; % A matrix corresponding to the state matrix used
C = [1 0 0 0; 0 1 0 0]; % transformation matrix to retain only the measured values
Z = [measured_x measured_y];    % Measurement matrix
P = [10^2 0 0 0; 0 10^2 0 0; 0 0 (v_max/3)^2 0; 0 0 0 (v_max/3)^2]; % initialised covariance matrix
Q = Q0 * [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];  % process noise variance matrix
R = [std_measured_x^2 0; 0 std_measured_y^2];   % measurement noise matrix

%creating result array
res_x = zeros(32,1);
res_y = zeros(32,1);

%storing the initial prediction values into the result
res_x(1) = X(1,1);
res_y(1) = X(2,1); 

%============================= start of algorithm ===============================
for i = 1:31

    % ------- prediction (priori estimate) -------
    X_priori = A*X; % predicted state BEFORE measurement using mathematical model
    P_predict = A*P*transpose(A)+Q; % predicted covariance matrix
    
    %----- update (posteriori estimate) -------
    %caluculating Kalman gain
    K_denominator = C*P_predict*transpose(C) + R; % denominator of Kalman gain
    K = P_predict*transpose(C)*pinv(K_denominator); %Kalman gain
    
    %updating state and covariance
    E = [Z(i,1); Z(i,2)] - (C*X_priori);
    %E = [measured_x(i); measured_y(i)] - (C*X_priori); % Innovation residual(i.e. error term)
    X = X_priori + K*E; % update posterior estimate for state matrix
    P = (eye(4) - K*C)*P_predict; % update covariance matrix
    
    %storing of results
    res_x(i+1) = X(1,1);
    res_y(i+1) = X(2,1);

end
%============================= end of algorithm ===============================
%Plotting of graph
plot(groundT_x, groundT_y, 'k',res_x, res_y, 'r- .');