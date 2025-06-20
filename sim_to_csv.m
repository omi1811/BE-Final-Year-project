% Define headers for your data columns (customize as needed)
headers = {'AC_Power', 'DC_Power', 'Module_Temp', 'Irradiation'};  

% Extract latest data row from simout
latest_row = sim_data(end, :);

% File name
filename = 'final_output.csv';

% Check if file exists
file_exists = isfile(filename);

% Open file in append mode
fileID = fopen(filename, 'a');

% If it's a new file, write headers first
if ~file_exists
    fprintf(fileID, '%s,', headers{1:end-1});
    fprintf(fileID, '%s\n', headers{end});
end


% Write the latest row of data
fprintf(fileID, '%f,', latest_row(1:end-1));
fprintf(fileID, '%f\n', latest_row(end));

% Close file
fclose(fileID);



