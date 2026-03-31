% =========================================================
% KCropAI: Agricultural Expert System Knowledge Base
% Course: CSA2001 Fundamentals in AI and ML
% Description: Defines environmental rules for Kerala crops
% =========================================================

% --- 1. FACTS (Objects and Predicates) ---
% Defines the crops available in our dataset.
crop(coconut).
crop(rubber).
crop(black_pepper).
crop(rice).
crop(banana).
crop(tapioca).
crop(coffee).

% Defines the ideal soil type for each crop.
soil_type(coconut, laterite).
soil_type(rubber, laterite).
soil_type(black_pepper, laterite).
soil_type(coffee, laterite).
soil_type(rice, alluvial).
soil_type(banana, alluvial).
soil_type(tapioca, red).

% Defines the rainfall requirement for each crop.
rainfall_req(coconut, high).
rainfall_req(rubber, high).
rainfall_req(black_pepper, high).
rainfall_req(rice, high).
rainfall_req(banana, moderate).
rainfall_req(tapioca, moderate).
rainfall_req(coffee, moderate).

% --- 2. RULES (Inference and Unification) ---
% Recommend a crop based on exact soil and rainfall conditions.
recommend_crop(Soil, Rainfall, Crop) :-
    crop(Crop),
    soil_type(Crop, Soil),
    rainfall_req(Crop, Rainfall).

% Identify crops suitable for heavy monsoon regions.
monsoon_crop(Crop) :-
    crop(Crop),
    rainfall_req(Crop, high).

% --- 3. LIST OPERATIONS (Lab Requirements) ---
% Use 'findall' to gather all crops matching a soil type into a List.
crops_for_soil(Soil, CropList) :-
    findall(C, soil_type(C, Soil), CropList).

% Recursive rule to check if a crop is in a given list.
is_in_list(X, [X|_]).
is_in_list(X, [_|Tail]) :- is_in_list(X, Tail).