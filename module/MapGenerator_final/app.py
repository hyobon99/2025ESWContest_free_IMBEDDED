import random
import utils

# --- 기존 글로벌 변수 및 상수 ---
# map_size = 16 # 예시: 함수 파라미터로 대체됨
# initial_land = 0.5 # 예시: 함수 파라미터로 대체됨
# smoothing = 3 # 예시: 함수 파라미터로 대체됨
# relief = 4 # 예시: 함수 파라미터로 대체됨
# tribes = ['Vengir', 'Bardur', 'Oumaji'] # 예시: 함수 파라미터로 대체됨

tribes_list = ['Xin-xi', 'Imperius', 'Bardur', 'Oumaji', 'Kickoo', 'Hoodrick', 'Luxidoor', 'Vengir', 'Zebasi',
               'Ai-mo', 'Quetzali', 'Yadakk', 'Aquarion', 'Elyrion', 'Polaris']

terrain = ['forest', 'fruit', 'game', 'ground', 'mountain']
general_terrain = ['crop', 'fish', 'metal', 'ocean', 'ruin', 'village', 'water', 'whale']

_____ = 2
____ = 1.5
___ = 1
__ = 0.5
_ = 0.1

BORDER_EXPANSION = 1 / 3

terrain_probs = {'water': {'Xin-xi': 0, 'Imperius': 0, 'Bardur': 0, 'Oumaji': 0, 'Kickoo': 0.4,
                           'Hoodrick': 0, 'Luxidoor': 0, 'Vengir': 0, 'Zebasi': 0, 'Ai-mo': 0,
                           'Quetzali': 0, 'Yadakk': 0, 'Aquarion': 0.3, 'Elyrion': 0, 'Polaris': 0.2}, # Polaris 추가
                 'forest': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': _, 'Kickoo': ___,
                            'Hoodrick': ____, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': __, 'Ai-mo': ___,
                            'Quetzali': ___, 'Yadakk': __, 'Aquarion': __, 'Elyrion': ___, 'Polaris': _},
                 'mountain': {'Xin-xi': ____, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': __,
                              'Hoodrick': __, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': __, 'Ai-mo': ____,
                              'Quetzali': ___, 'Yadakk': __, 'Aquarion': ___, 'Elyrion': __, 'Polaris': ___},
                 'metal': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': _____, 'Zebasi': ___, 'Ai-mo': ___,
                           'Quetzali': _, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___, 'Polaris': ___},
                 'fruit': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ____, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': _____, 'Vengir': _, 'Zebasi': __, 'Ai-mo': ___,
                           'Quetzali': _____, 'Yadakk': ____, 'Aquarion': ___, 'Elyrion': ___, 'Polaris': _},
                 'crop': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': _, 'Oumaji': ___, 'Kickoo': ___,
                          'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': ___, 'Ai-mo': _,
                          'Quetzali': _, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ____, 'Polaris': _},
                 'game': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': _____, 'Oumaji': ___, 'Kickoo': ___,
                          'Hoodrick': ___, 'Luxidoor': __, 'Vengir': _, 'Zebasi': ___, 'Ai-mo': ___,
                          'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___, 'Polaris': ____},
                 'fish': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ____,
                          'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': _, 'Zebasi': ___, 'Ai-mo': ___,
                          'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___, 'Polaris': ___},
                 'whale': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': ___, 'Ai-mo': ___,
                           'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___, 'Polaris': __}}


general_probs = {'mountain': 0.15, 'forest': 0.4, 'fruit': 0.5, 'crop': 0.5,
                 'fish': 0.5, 'game': 0.5, 'whale': 0.4, 'metal': 0.5}

# --- 전체 맵 생성 로직을 포함하는 함수 ---
def create_full_map(map_size, initial_land, smoothing, relief, tribes_param, 
                      fill_tribe=None, no_biomes=False, no_resources=False):
    
    world_map = [{'type': 'ocean', 'above': None, 'road': False, 'tribe': fill_tribe if fill_tribe else 'Xin-xi'} 
                 for _ in range(map_size ** 2)]

    # 초기 육지 타일 배치
    j = 0
    while j < map_size ** 2 * initial_land:
        cell = random.randrange(0, map_size ** 2)
        if world_map[cell]['type'] == 'ocean':
            j += 1
            world_map[cell]['type'] = 'ground'

    land_coefficient = (0.5 + relief) / 9

    # 스무딩 반복
    for _ in range(smoothing):
        temp_roads = [False] * (map_size ** 2) # road 마킹용 임시 리스트
        for cell in range(map_size ** 2):
            water_count = 0
            tile_count = 0
            # utils.round_는 utils.py에 정의되어 있다고 가정
            neighbours = utils.round_(cell, 1, map_size)
            for i_neighbor in range(len(neighbours)): # 변수명 변경 i -> i_neighbor
                if neighbours[i_neighbor] == cell: continue # 자기 자신 제외
                if world_map[neighbours[i_neighbor]]['type'] == 'ocean':
                    water_count += 1
                tile_count += 1
            if tile_count > 0 and (water_count / tile_count <= land_coefficient):
                temp_roads[cell] = True # road로 마킹 (ground가 될 후보)
        
        for cell in range(map_size ** 2):
            if temp_roads[cell]:
                world_map[cell]['type'] = 'ground'
            else:
                world_map[cell]['type'] = 'ocean'

    capital_cells = []
    # 단일 부족으로 채우는 경우가 아닐 때만 수도 및 영역 분배
    if not fill_tribe:
        capital_map = {}
        # 수도 후보 셀 검색 (맵 중앙 영역)
        for tribe in tribes_param: # 함수 인자로 받은 tribes_param 사용
            for row in range(2, map_size - 2):
                for column in range(2, map_size - 2):
                    cell_idx = row * map_size + column
                    if world_map[cell_idx]['type'] == 'ground':
                        capital_map[cell_idx] = 0 # 점수/거리 대신 단순 후보로 표시
        
        # 부족별 수도 배정
        current_capital_candidates = list(capital_map.keys())
        random.shuffle(current_capital_candidates)

        for tribe in tribes_param:
            if not current_capital_candidates: break # 후보지가 없으면 중단

            best_cell = -1
            max_min_dist = -1

            if not capital_cells: # 첫번째 수도
                if current_capital_candidates:
                    best_cell = random.choice(current_capital_candidates)
            else:
                potential_cells_with_scores = []
                for cand_cell in current_capital_candidates:
                    min_dist_to_existing = map_size * 2 # 충분히 큰 값
                    for cap_cell in capital_cells:
                        min_dist_to_existing = min(min_dist_to_existing, utils.distance(cand_cell, cap_cell, map_size))
                    potential_cells_with_scores.append({'cell': cand_cell, 'score': min_dist_to_existing})
                
                if potential_cells_with_scores:
                    potential_cells_with_scores.sort(key=lambda x: x['score'], reverse=True)
                    # 가장 먼 셀들 중 랜덤 선택
                    highest_score = potential_cells_with_scores[0]['score']
                    top_candidates = [c['cell'] for c in potential_cells_with_scores if c['score'] == highest_score]
                    if top_candidates:
                        best_cell = random.choice(top_candidates)

            if best_cell != -1:
                capital_cells.append(best_cell)
                world_map[best_cell]['above'] = 'capital'
                world_map[best_cell]['tribe'] = tribe
                if best_cell in current_capital_candidates: # 후보에서 제거
                    current_capital_candidates.remove(best_cell)
            # else: 수도를 놓을 자리가 없음 (무시하고 다음 부족으로)

        # 영역 확장 (Terrain distribution)
        if capital_cells: # 수도가 하나라도 배정된 경우에만 영역 확장
            done_tiles = list(capital_cells) 
            active_tiles_per_tribe = {} # 부족별 active_tiles 관리
            tribe_indices = {tribe_name: i for i, tribe_name in enumerate(tribes_param)}

            for capital_idx, cell_idx in enumerate(capital_cells):
                tribe_of_capital = world_map[cell_idx]['tribe']
                if tribe_of_capital not in active_tiles_per_tribe:
                    active_tiles_per_tribe[tribe_of_capital] = []
                active_tiles_per_tribe[tribe_of_capital].append(cell_idx)

            # 모든 타일이 채워질 때까지 또는 더 이상 확장이 불가능할 때까지
            while len(done_tiles) < map_size ** 2:
                expanded_in_this_iteration = False
                for tribe_name in tribes_param:
                    if tribe_name == 'Polaris' or tribe_name not in active_tiles_per_tribe or not active_tiles_per_tribe[tribe_name]:
                        continue

                    # 확장할 셀 랜덤 선택 (해당 부족의 active_tiles 중에서)
                    rand_cell_from_active = random.choice(active_tiles_per_tribe[tribe_name])
                    neighbours = utils.circle(rand_cell_from_active, 1, map_size)
                    
                    valid_neighbours = [n for n in neighbours if n not in done_tiles and world_map[n]['type'] != 'water'] # 원본 로직: 물이 아닌 곳
                    if not valid_neighbours: # 물이 아닌 곳이 없으면, 물이라도 확장 대상
                        valid_neighbours = [n for n in neighbours if n not in done_tiles]

                    if valid_neighbours:
                        new_expanded_cell = random.choice(valid_neighbours)
                        world_map[new_expanded_cell]['tribe'] = tribe_name
                        active_tiles_per_tribe[tribe_name].append(new_expanded_cell)
                        done_tiles.append(new_expanded_cell)
                        expanded_in_this_iteration = True
                    else: # 더 이상 확장할 곳이 없는 타일
                        active_tiles_per_tribe[tribe_name].remove(rand_cell_from_active)
                
                if not expanded_in_this_iteration and len(done_tiles) < map_size ** 2 : # 교착 상태 방지
                    # 아직 할당되지 않은 타일이 있다면, 가장 가까운 기존 영역에 편입시키거나 랜덤 할당
                    remaining_tiles = [i for i in range(map_size**2) if i not in done_tiles]
                    if not remaining_tiles: break
                    
                    # 간단히 첫번째 부족 또는 랜덤 부족으로 채우기 (개선 필요)
                    # 이 부분은 index.js의 fill 로직과 유사하게 처리하거나, 더 정교한 로직이 필요할 수 있습니다.
                    # 여기서는 임시로 남은 타일을 가장 가까운 부족에게 할당 시도 (매우 단순화된 버전)
                    if tribes_param:
                         for tile_to_fill in remaining_tiles:
                            if tile_to_fill in done_tiles: continue
                            # 가장 가까운 done_tile을 찾아 그 부족으로 할당 (성능에 영향 줄 수 있음)
                            min_dist = map_size * 2
                            closest_tribe = None
                            for dt in done_tiles:
                                d = utils.distance(tile_to_fill, dt, map_size)
                                if d < min_dist:
                                    min_dist = d
                                    closest_tribe = world_map[dt]['tribe']
                            if closest_tribe :
                                world_map[tile_to_fill]['tribe'] = closest_tribe
                                done_tiles.append(tile_to_fill)
                                expanded_in_this_iteration = True # 다시 확장 루프 돌도록
                    if not expanded_in_this_iteration: # 그래도 확장이 안되면 루프 종료
                         break


    # 생물 군계 생성 (no_biomes 플래그에 따라)
    if not no_biomes:
        for cell in range(map_size**2):
            # fill_tribe의 경우에도 바이옴 생성은 적용될 수 있음 (기존 로직 기반)
            current_tribe = world_map[cell]['tribe']
            if not current_tribe : current_tribe = 'Xin-xi' # 기본값

            if world_map[cell]['type'] == 'ground' and world_map[cell]['above'] is None:
                rand = random.random()
                if rand < general_probs['forest'] * terrain_probs['forest'].get(current_tribe, 0.1): # .get으로 안전하게 접근
                    world_map[cell]['type'] = 'forest'
                elif rand > 1 - general_probs['mountain'] * terrain_probs['mountain'].get(current_tribe, 0.1):
                    world_map[cell]['type'] = 'mountain'
                
                rand = random.random()
                if rand < terrain_probs['water'].get(current_tribe, 0):
                    world_map[cell]['type'] = 'ocean' # 나중에 water로 바뀔 수 있음

    # 얕은 물(water)로 변경
    land_like_terrain = ['ground', 'forest', 'mountain']
    for cell in range(map_size**2):
        if world_map[cell]['type'] == 'ocean':
            for neighbour in utils.plus_sign(cell, map_size):
                if world_map[neighbour]['type'] in land_like_terrain:
                    world_map[cell]['type'] = 'water'
                    break
    
    # 자원 및 마을 배치 (no_resources 플래그에 따라)
    if not no_resources:
        village_map = [-1] * (map_size**2) # -1: 배치불가, 0: 가능, 1:외곽, 2:근처, 3:중심
        if not fill_tribe : # fill_tribe일때는 마을/자원생성 스킵 (index.js 동작 참고)
            for cell in range(map_size**2):
                row = cell // map_size
                column = cell % map_size
                if world_map[cell]['type'] == 'ocean' or world_map[cell]['type'] == 'mountain':
                    village_map[cell] = -1
                elif row == 0 or row == map_size - 1 or column == 0 or column == map_size - 1:
                    village_map[cell] = -1
                else:
                    village_map[cell] = 0 # 배치 가능

            # 수도 주변 마을 배치 우선순위
            for capital in capital_cells:
                village_map[capital] = 3 
                for cell_around in utils.circle(capital, 1, map_size):
                     if 0 <= cell_around < map_size**2: village_map[cell_around] = max(village_map[cell_around], 2)
                for cell_around in utils.circle(capital, 2, map_size):
                     if 0 <= cell_around < map_size**2: village_map[cell_around] = max(village_map[cell_around], 1)
            
            # 나머지 지역 마을 배치
            village_count = 0
            possible_village_spots = [i for i, val in enumerate(village_map) if val == 0]
            random.shuffle(possible_village_spots)
            
            # 대략적인 마을 수 (맵 크기에 비례, 조절 가능)
            num_villages_to_place = map_size # 예시 값
            
            for new_village_idx in possible_village_spots:
                if village_map[new_village_idx] == 0 : # 아직 마을이거나 영향권이 아닌 경우
                    village_map[new_village_idx] = 3
                    for cell_around in utils.circle(new_village_idx, 1, map_size):
                        if 0 <= cell_around < map_size**2: village_map[cell_around] = max(village_map[cell_around], 2)
                    for cell_around in utils.circle(new_village_idx, 2, map_size):
                        if 0 <= cell_around < map_size**2: village_map[cell_around] = max(village_map[cell_around], 1)
                    village_count +=1
                    if village_count >= num_villages_to_place:
                        break
            
            # 자원 생성 함수 (proc 유사)
            def check_proc(cell_idx, probability):
                if not (0 <= village_map[cell_idx] <= 2) : return False # -1(배치불가)이거나 3(마을중심)이면 자원X
                
                # village_map 값이 2 (initial territory) 또는 1 (border expansion)
                # index.js: (village_map[cell_] == 2 && random.random() < probability) or (village_map[cell_] == 1 && random.random() < probability * BORDER_EXPANSION)
                # 여기서는 village_map의 값에 따라 가중치를 둘 수 있지만, 우선은 동일 확률로 처리
                # 또는, 수도/마을에서 가까울수록 확률을 높이는 등으로 수정 가능.
                # 지금은 1, 2 모두 동일한 확률로 처리하되, 마을 중심(3)과 배치불가(-1)는 제외
                
                if village_map[cell_idx] == 2 and random.random() < probability: return True
                if village_map[cell_idx] == 1 and random.random() < probability * BORDER_EXPANSION: return True
                return False

            # 각 셀에 자원 배치
            for cell in range(map_size**2):
                current_tribe = world_map[cell]['tribe']
                if not current_tribe: current_tribe = 'Xin-xi' # 기본값

                if world_map[cell]['above'] == 'capital': continue # 수도 위에는 자원 X

                cell_type = world_map[cell]['type']
                
                if village_map[cell] == 3 : # 마을 중심지
                     if cell_type == 'forest': world_map[cell]['type'] = 'ground' # 숲 위 마을은 땅으로
                     world_map[cell]['above'] = 'village'
                     continue

                if cell_type == 'ground':
                    fruit_prob = general_probs['fruit'] * terrain_probs['fruit'].get(current_tribe, 0.1)
                    crop_prob = general_probs['crop'] * terrain_probs['crop'].get(current_tribe, 0.1)
                    if check_proc(cell, fruit_prob * (1 - crop_prob / 2)): # 원본 index.js 로직 참고
                        world_map[cell]['above'] = 'fruit'
                    elif check_proc(cell, crop_prob * (1 - fruit_prob / 2)):
                        world_map[cell]['above'] = 'crop'
                elif cell_type == 'forest':
                    if check_proc(cell, general_probs['game'] * terrain_probs['game'].get(current_tribe, 0.1)):
                        world_map[cell]['above'] = 'game'
                elif cell_type == 'water':
                    if check_proc(cell, general_probs['fish'] * terrain_probs['fish'].get(current_tribe, 0.1)):
                        world_map[cell]['above'] = 'fish'
                elif cell_type == 'ocean':
                    if check_proc(cell, general_probs['whale'] * terrain_probs['whale'].get(current_tribe, 0.1)): # 확률 낮음
                        world_map[cell]['above'] = 'whale'
                elif cell_type == 'mountain':
                    if check_proc(cell, general_probs['metal'] * terrain_probs['metal'].get(current_tribe, 0.1)):
                        world_map[cell]['above'] = 'metal'
            
            # 유적 배치
            ruins_number = round(map_size**2 / 40)
            water_ruins_number = round(ruins_number / 3)
            ruins_count = 0
            water_ruins_count = 0
            
            # 유적 배치 가능 지역 (마을 중심(3), 근처(2) 제외. 외곽(1)이나 영향없는(0) 또는 배치불가(-1) 지역)
            possible_ruin_spots = [i for i, val in enumerate(village_map) if val <= 1]
            random.shuffle(possible_ruin_spots)

            for ruin_candidate_idx in possible_ruin_spots:
                if ruins_count >= ruins_number: break
                
                terrain_type_at_ruin = world_map[ruin_candidate_idx]['type']
                # 물 위가 아니거나, 아직 바다 유적 수가 부족한 경우만 배치
                if terrain_type_at_ruin != 'water' and \
                   (water_ruins_count < water_ruins_number or terrain_type_at_ruin != 'ocean'):
                    if world_map[ruin_candidate_idx]['above'] is None : # 다른 자원이 없는 곳에 우선 배치
                        world_map[ruin_candidate_idx]['above'] = 'ruin'
                        if terrain_type_at_ruin == 'ocean':
                            water_ruins_count += 1
                        
                        # 유적 주변 village_map 값 조정 (index.js 참고) - 여기서는 생략 가능 (이미 자원배치 끝)
                        # for c_around in utils.circle(ruin_candidate_idx, 1, map_size):
                        #    if 0 <= c_around < map_size**2: village_map[c_around] = max(village_map[c_around], 2)
                        ruins_count += 1
        
            # 부족별 특화 자원 배치 (post_generate 유사 로직)
            def check_res_count(resource_type, capital_idx):
                count = 0
                for n_idx in utils.circle(capital_idx, 1, map_size): # 수도 주변 1칸
                    if 0 <= n_idx < map_size**2 and world_map[n_idx]['above'] == resource_type:
                        count +=1
                return count

            def place_specific_resource(resource_type, on_terrain_type, quantity, capital_idx):
                placed_count = check_res_count(resource_type, capital_idx)
                attempts = 0 # 무한루프 방지
                
                possible_placement_indices = [
                    idx for idx in utils.circle(capital_idx, 1, map_size) 
                    if 0 <= idx < map_size**2 and world_map[idx]['above'] is None # 빈 타일에만
                ]
                random.shuffle(possible_placement_indices)

                for place_idx in possible_placement_indices:
                    if placed_count >= quantity or attempts > 20: break
                    
                    world_map[place_idx]['type'] = on_terrain_type
                    world_map[place_idx]['above'] = resource_type
                    placed_count +=1
                    attempts +=1
                    
                    # 주변이 바다면 물로 (Kickoo 로직 참고)
                    # for n_idx in utils.plus_sign(place_idx, map_size):
                    #    if 0 <= n_idx < map_size**2 and world_map[n_idx]['type'] == 'ocean':
                    #        world_map[n_idx]['type'] = 'water'
                return placed_count


            for capital_idx in capital_cells:
                tribe = world_map[capital_idx]['tribe']
                if tribe == 'Imperius':
                    place_specific_resource('fruit', 'ground', 2, capital_idx)
                elif tribe == 'Bardur':
                    place_specific_resource('game', 'forest', 2, capital_idx)
                elif tribe == 'Kickoo':
                    # Kickoo는 물고기 2개 보장 (주변을 water로 만들면서)
                    fish_count = check_res_count('fish', capital_idx)
                    attempts = 0
                    plus_neighbors = utils.plus_sign(capital_idx, map_size) # 상하좌우
                    random.shuffle(plus_neighbors)

                    for neighbor_idx in plus_neighbors:
                        if fish_count >= 2 or attempts >= 8: break
                        if 0 <= neighbor_idx < map_size**2 and world_map[neighbor_idx]['above'] is None:
                             # Kickoo는 물가가 아니어도 물고기를 위해 물로 바꿀 수 있음
                            world_map[neighbor_idx]['type'] = 'water'
                            world_map[neighbor_idx]['above'] = 'fish'
                            fish_count +=1
                        attempts +=1
                elif tribe == 'Zebasi':
                    place_specific_resource('crop', 'ground', 1, capital_idx)
                elif tribe == 'Elyrion':
                    # Elyrion은 game 2개지만, index.js에선 일반 game 자원 로직으로 처리됨.
                    # 여기서는 Bardur와 유사하게 처리하거나, Elyrion만의 특성을 넣을 수 있음.
                    # 예: 숲이 아닌 곳에도 game을 생성 (단, paintEvent가 숲 위에 그리는것과 충돌 가능)
                    # 현재는 일반적인 game 생성 로직에 의존. 추가적인 처리는 필요시 구현.
                    place_specific_resource('game', 'forest', 1, capital_idx) # 일단 1개 추가 시도
                    pass 
                elif tribe == 'Polaris': # Polaris는 주변 1칸을 자기 부족 영역으로 (이미 territory expansion에서 처리되었을 수 있음)
                    for neighbour_idx in utils.circle(capital_idx, 1, map_size):
                        if 0 <= neighbour_idx < map_size**2 :
                             world_map[neighbour_idx]['tribe'] = 'Polaris'
                             # Polaris는 주변을 얼음(예: mountain type 변형)으로 만들 수 있음
                             # if world_map[neighbour_idx]['type'] in ['ground', 'forest']:
                             #    world_map[neighbour_idx]['type'] = 'mountain' # 임시로 산으로 표시 (얼음 이미지 필요)


    # Polaris의 경우 주변을 얼음 땅으로 바꾸는 로직 (예시)
    # 이 부분은 terrain_probs['water'] for Polaris와 함께 조정되어야 합니다.
    # 또는 'ice'라는 새로운 지형 타입을 만들고 해당 이미지를 사용해야 합니다.
    # 지금은 Polaris가 자신의 영역을 'water' 또는 'mountain'으로 바꾸는 경향이 있도록 terrain_probs를 조정했습니다.
    # 추가적으로, 수도 주변을 강제로 특정 지형으로 바꾸는 로직도 넣을 수 있습니다.
    for cell_idx in range(map_size**2):
        if world_map[cell_idx]['tribe'] == 'Polaris':
            # 예: Polaris 영역의 ground/forest를 mountain(얼음처럼 보이게)으로 바꾸거나 water로.
            if world_map[cell_idx]['type'] in ['ground', 'forest']:
                 if random.random() < 0.3: # 30% 확률로 산(얼음)으로
                      world_map[cell_idx]['type'] = 'mountain' 
                 elif random.random() < 0.2: # 20% 확률로 물로 (얼음이 녹은 물 또는 얼지 않은 물)
                      world_map[cell_idx]['type'] = 'water'


    return world_map

# --- 기존 generate_map 함수는 제거됨 ---
# def generate_map(world_map, map_size, initial_land, smoothing, relief, tribes):
#    ... (내용 삭제) ...


# 이 파일이 직접 실행될 때 (테스트용)
if __name__ == '__main__':
    test_map_size = 16
    test_initial_land = 0.4
    test_smoothing = 3
    test_relief = 4
    test_tribes = ['Vengir', 'Bardur', 'Oumaji', 'Kickoo', 'Xin-xi']
    
    # Polaris 테스트
    # test_tribes = ['Polaris', 'Bardur']


    print(f"테스트 맵 생성 시작: size={test_map_size}, land={test_initial_land}, tribes={test_tribes}")
    
    # full_world_map = create_full_map(test_map_size, test_initial_land, test_smoothing, test_relief, test_tribes)
    full_world_map = create_full_map(
        map_size=test_map_size, 
        initial_land=test_initial_land, 
        smoothing=test_smoothing, 
        relief=test_relief, 
        tribes_param=test_tribes,
        fill_tribe=None, # 또는 'Xin-xi' 등으로 테스트
        no_biomes=False,
        no_resources=False
    )

    print(f"맵 생성 완료. 총 {len(full_world_map)}개의 타일.")
    
    # 간단한 텍스트 출력 (mapGeneration.py의 paintEvent가 시각화 담당)
    capitals_found = 0
    tribes_on_map = set()
    resources_counts = {}

    for i, cell_data in enumerate(full_world_map):
        if (i % test_map_size) == 0:
            print() # 줄바꿈
        
        char_to_print = '.' # 기본 바다 또는 빈 땅
        if cell_data['type'] == 'ground': char_to_print = 'g'
        elif cell_data['type'] == 'forest': char_to_print = 'f'
        elif cell_data['type'] == 'mountain': char_to_print = 'm'
        elif cell_data['type'] == 'water': char_to_print = 'w'
        elif cell_data['type'] == 'ocean': char_to_print = 'o'

        if cell_data['above'] == 'capital':
            char_to_print = cell_data['tribe'][0] # 부족 첫글자 (대문자)
            capitals_found +=1
        elif cell_data['above'] == 'village':
            char_to_print = 'v'
        elif cell_data['above']: # 기타 자원
            char_to_print = cell_data['above'][0] # 자원 첫글자 (소문자)
            resources_counts[cell_data['above']] = resources_counts.get(cell_data['above'], 0) + 1
            
        print(char_to_print, end=' ')
        if cell_data['tribe']:
            tribes_on_map.add(cell_data['tribe'])
    
    print(f"\n\n수도 개수: {capitals_found}")
    print(f"맵 위의 부족들: {tribes_on_map}")
    print(f"자원 분포: {resources_counts}")
    # print(full_world_map[:5]) # 처음 5개 타일 데이터
