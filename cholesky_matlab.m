function [] = cholesky_matlab()
    if(ispc)
        system = 'Windows';
    elseif(ismac)
        system = 'Darwin';
    else
        system = 'Linux';
    end

    % Global variables
    INPUT_DIRECTORY = '/Users/';
    MATRICES_NAMES = ["ex15" "shallow_water1" "apache2" "parabolic_fem" "G3_circuit" "cfd1" "cfd2" "StocF-1465" "Flan_1565"];
    OUTPUT_PATH = strcat(INPUT_DIRECTORY, 'data_matlab_', lower(system), '.csv');
    CSV_HEADER = {'Environment' 'System' 'Matrix name' 'Elapsed time (s)' 'Memory (MB)' 'Relative error'};
    CSV_HEADER = [CSV_HEADER;repmat({','}, 1, numel(CSV_HEADER))];
    CSV_HEADER = cell2mat(CSV_HEADER(:)');
    CSV_HEADER = CSV_HEADER(1 : end-1);
    
    csv_file = fopen(OUTPUT_PATH, 'w');
    fprintf(csv_file, '%s\n', CSV_HEADER);
    
    for matrix = MATRICES_NAMES
        [time, memory, error] = resolve(strcat(INPUT_DIRECTORY, matrix));
        
        info = ['MATLAB' system matrix time memory error];
        [rows, ~] = size(info);
        for i=1 : rows
              fprintf(csv_file, '%s,', info{i,1:end-1});
              fprintf(csv_file,'%s\n', info{i,end});
        end
        
        sprintf('Environment: MATLAB\nSystem: %s\nMatrix: %s\nElapsed time: %.8f s\nMemory: %.2f MB\nRelative error: %d\n', system, matrix, time, memory, error)
    end
    
    fclose(csv_file);
end

function [time, memory, error] = resolve(matrix_path)
    M = load(matrix_path);
    A = M.Problem.A;
    clear M;

    start_memory = whos;
    start_memory = sum([start_memory.bytes]);
    
    xe = ones(length(A), 1);
    b = A * xe;
    
    tic
    
    [R, ~, P] = chol(A, 'lower');
    x = P * (R' \ (R \ (P' * b)));
    % x = A \ b; % mldivide
        
    time = toc;
    
    error = norm(x - xe) / norm(xe);

    end_memory = whos;
    end_memory = sum([end_memory.bytes]);
    memory = (end_memory - start_memory) / (1024 * 1024);
end