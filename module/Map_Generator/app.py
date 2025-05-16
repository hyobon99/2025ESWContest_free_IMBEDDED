import random
import utils

map_size = 16  # int(input('Enter map size (16): '))                                        # 맵의 한 변 길이 (전체 타일 수는 map_size ** 2)
initial_land = 0.5  # float(input('Enter initial land (0.5): '))                            # 초기 육지 비율 (0.0 ~ 1.0)
smoothing = 3  # int(input('Enter smoothing (3): '))                                        # 지형을 얼마나 부드럽게 만들지 (스무딩 반복 횟수)
relief = 4  # int(input('Enter relief (4): '))                                              # 지형의 기복 정도
tribes = ['Vengir', 'Bardur', 'Oumaji']  # list(map(str, input('Enter tribes: ').split()))  # 사용할 부족 목록(-> 추후 유저 캐릭터로 교체)

tribes_list = ['Xin-xi', 'Imperius', 'Bardur', 'Oumaji', 'Kickoo', 'Hoodrick', 'Luxidoor', 'Vengir', 'Zebasi',
               'Ai-mo', 'Quetzali', 'Yadakk', 'Aquarion', 'Elyrion', 'Polaris']             # 전체 부족 목록 (추후 전체 캐릭터 목록으로 교체)

terrain = ['forest', 'fruit', 'game', 'ground', 'mountain']                                 # 기본 지형 종류
general_terrain = ['crop', 'fish', 'metal', 'ocean', 'ruin', 'village', 'water', 'whale']   # 기본 자원 종류


# 확률 값용 상수 정의 (가독성을 높이기 위한 변수 이름)
_____ = 2
____ = 1.5
___ = 1
__ = 0.5
_ = 0.1

BORDER_EXPANSION = 1 / 3    # 국경 확장의 확률 보정값

# 부족별 지형 등장 확률 정의 
terrain_probs = {'water': {'Xin-xi': 0, 'Imperius': 0, 'Bardur': 0, 'Oumaji': 0, 'Kickoo': 0.4,
                           'Hoodrick': 0, 'Luxidoor': 0, 'Vengir': 0, 'Zebasi': 0, 'Ai-mo': 0,
                           'Quetzali': 0, 'Yadakk': 0, 'Aquarion': 0.3, 'Elyrion': 0},
                 'forest': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': _, 'Kickoo': ___,
                            'Hoodrick': ____, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': __, 'Ai-mo': ___,
                            'Quetzali': ___, 'Yadakk': __, 'Aquarion': __, 'Elyrion': ___},
                 'mountain': {'Xin-xi': ____, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': __,
                              'Hoodrick': __, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': __, 'Ai-mo': ____,
                              'Quetzali': ___, 'Yadakk': __, 'Aquarion': ___, 'Elyrion': __},
                 'metal': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': _____, 'Zebasi': ___, 'Ai-mo': ___,
                           'Quetzali': _, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___},
                 'fruit': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ____, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': _____, 'Vengir': _, 'Zebasi': __, 'Ai-mo': ___,
                           'Quetzali': _____, 'Yadakk': ____, 'Aquarion': ___, 'Elyrion': ___},
                 'crop': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': _, 'Oumaji': ___, 'Kickoo': ___,
                          'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': ___, 'Ai-mo': _,
                          'Quetzali': _, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ____},
                 'game': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': _____, 'Oumaji': ___, 'Kickoo': ___,
                          'Hoodrick': ___, 'Luxidoor': __, 'Vengir': _, 'Zebasi': ___, 'Ai-mo': ___,
                          'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___},
                 'fish': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ____,
                          'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': _, 'Zebasi': ___, 'Ai-mo': ___,
                          'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___},
                 'whale': {'Xin-xi': ___, 'Imperius': ___, 'Bardur': ___, 'Oumaji': ___, 'Kickoo': ___,
                           'Hoodrick': ___, 'Luxidoor': ___, 'Vengir': ___, 'Zebasi': ___, 'Ai-mo': ___,
                           'Quetzali': ___, 'Yadakk': ___, 'Aquarion': ___, 'Elyrion': ___}}

# 일반 자원의 기본 등장 확률
general_probs = {'mountain': 0.15, 'forest': 0.4, 'fruit': 0.5, 'crop': 0.5,
                 'fish': 0.5, 'game': 0.5, 'whale': 0.4, 'metal': 0.5}

# 맵을 ocean(바다)으로 초기화
world_map = [{'type': 'ocean', 'above': None, 'road': False, 'tribe': 'Xin-xi'} for i in range(map_size ** 2)]

# 초기 육지 타일 배치 (비율에 따라 ocean → ground로 일부 전환)
j = 0
while j < map_size ** 2 * initial_land:
    cell = random.randrange(0, map_size ** 2)
    if world_map[cell]['type'] == 'ocean':
        j += 1
        world_map[cell]['type'] = 'ground'

# 육지/바다의 비율 조절 계수 계산 (지형 스무딩 시 활용)
land_coefficient = (0.5 + relief) / 9

# 스무딩 반복
for i in range(smoothing):
    # 주변 바다 비율에 따라 현재 셀을 road로 마킹
    for cell in range(map_size ** 2):
        water_count = 0
        tile_count = 0
        neighbours = utils.round_(cell, 1, map_size)
        for i in range(len(neighbours)):
            if world_map[neighbours[i]]['type'] == 'ocean':
                water_count += 1
            tile_count += 1
        if water_count / tile_count <= land_coefficient:
            world_map[cell]['road'] = True

    # road로 마킹된 셀은 ground로, 나머지는 ocean으로 재설정
    for cell in range(map_size ** 2):
        if world_map[cell]['road']:
            world_map[cell]['road'] = False
            world_map[cell]['type'] = 'ground'
        else:
            world_map[cell]['type'] = 'ocean'

# 수도 후보 셀과 최종 수도 셀 목록 초기화
capital_cells = []
capital_map = {}

# 부족별로 수도 후보 셀을 맵 가운데 영역에서 검색
for tribe in tribes:
    for row in range(2, map_size - 2):
        for column in range(2, map_size - 2):
            if world_map[row * map_size + column]['type'] == 'ground':
                capital_map[row * map_size + column] = 0
                
# 부족별로 수도 하나씩 배정 (기존 수도들과 가장 멀리 떨어진 셀을 선택)
for tribe in tribes:
    max_ = 0
    for cell in capital_map:
        capital_map[cell] = map_size  # 초기 거리 설정
        for capital_cell in capital_cells:
            capital_map[cell] = min(capital_map[cell], utils.distance(cell, capital_cell, map_size))
        max_ = max(max_, capital_map[cell])
    
    # 가장 먼 셀들 중 랜덤하게 하나 선택
    len_ = 0
    for cell in capital_map:
        if capital_map[cell] == max_:
            len_ += 1
    rand_cell = random.randrange(0, len_)
    for cell in capital_map.items():
        if cell[1] == max_:
            if rand_cell == 0:
                capital_cells.append(int(cell[0]))
            rand_cell -= 1

# 각 수도 셀에 대해 지도에 표시 (above='capital' / tribe 지정)
for i in range(len(capital_cells)):
    world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['above'] = 'capital'
    world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['tribe'] = tribes[i]


# 부족별로 확장한 셀들을 추적하기 위한 리스트 초기화
done_tiles = []         # 이미 부족이 배정된 셀들의 집합
active_tiles = []       # 현재 확장 가능한 셀들을 저장 (초기에는 수도)

# 수도 위치를 시작점으로 설정
for i in range(len(capital_cells)):
    done_tiles.append(capital_cells[i])             # 수도 셀은 이미 확장된 셀로 처리
    active_tiles.append([capital_cells[i]])         # 각 부족의 초기 active 타일은 수도 하나뿐

# 전체 타일이 확장될 때까지 반복
while len(done_tiles) != map_size ** 2:
    for i in range(len(tribes)):
        # Polaris 부족은 예외 (확장하지 않음)
        if len(active_tiles[i]) and tribes[i] != 'Polaris':
            # 확장할 셀을 랜덤하게 선택
            rand_number = random.randrange(0, len(active_tiles[i]))
            rand_cell = active_tiles[i][rand_number]

            # 인접한 셀을 가져옴 (원형으로 radius=1 범위)
            neighbours = utils.circle(rand_cell, 1, map_size)

            # 아직 확장되지 않았고 물이 아닌 셀만 골라냄
            valid_neighbours = list(filter(lambda tile: tile not in done_tiles and
                                                   world_map[tile]['type'] != 'water', neighbours))
            
            # 만약 그런 셀이 없다면, 물이라도 괜찮으니 아무 셀이나 확장 대상으로 삼음
            if not len(valid_neighbours):
                valid_neighbours = list(filter(lambda tile: tile not in done_tiles, neighbours))

            # 확장 가능한 셀이 있다면
            if len(valid_neighbours):
                new_rand_number = random.randrange(0, len(valid_neighbours))
                new_rand_cell = valid_neighbours[new_rand_number]

                # 해당 셀을 현재 부족의 영역으로 설정
                world_map[new_rand_cell]['tribe'] = tribes[i]
                active_tiles[i].append(new_rand_cell)
                done_tiles.append(new_rand_cell)
            else:
                # 확장 불가능하면 해당 셀을 active 목록에서 제거
                active_tiles[i].remove(rand_cell)

# 부족 배정이 완료된 후, 각 셀의 지형 세부화를 진행
for cell in range(map_size**2):
    # 기본 육지(ground)이며 수도도 마을도 아닌 셀만 대상
    if world_map[cell]['type'] == 'ground' and world_map[cell]['above'] is None:
        rand = random.random()
        # 부족의 특성에 따라 확률적으로 forest로 바꿈
        if rand < general_probs['forest'] * terrain_probs['forest'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'forest'
        # 또는 확률적으로 mountain으로 바꿈
        elif rand > 1 - general_probs['mountain'] * terrain_probs['mountain'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'mountain'
        
        # 추가로 물(물가 지역)로 바꿀 수도 있음 (추가적 random)
        rand = random.random()
        if rand < terrain_probs['water'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'ocean'

# 각 셀의 마을 배치 가능 여부를 저장할 village_map 리스트 생성
village_map = []
for cell in range(map_size**2):
    row = cell // map_size
    column = cell % map_size
    # 바다(ocean)나 산(mountain) 위에는 마을을 배치할 수 없음 → -1
    if world_map[cell]['type'] == 'ocean' or world_map[cell]['type'] == 'mountain':
        village_map.append(-1)
    # 맵 테두리(가장자리)에도 마을 배치 불가 → -1
    elif row == 0 or row == map_size - 1 or column == 0 or column == map_size - 1:
        village_map.append(-1)
    else:
        village_map.append(0)  # 마을 배치 가능

# 'ocean' 셀 중에서 육지에 인접한 경우는 'water'로 변경 (얕은 물 표현)
land_like_terrain = ['ground', 'forest', 'mountain']
for cell in range(map_size**2):
    if world_map[cell]['type'] == 'ocean':
        for neighbour in utils.plus_sign(cell, map_size):  # 상하좌우 이웃 확인
            if world_map[neighbour]['type'] in land_like_terrain:
                world_map[cell]['type'] = 'water'  # 얕은 물로 변경
                break

# 수도 주변에 마을 배치 우선
village_count = 0
for capital in capital_cells:
    village_map[capital] = 3  # 수도가 위치한 셀은 마을 중심지로 표시 (우선순위 3)
    for cell in utils.circle(capital, 1, map_size):  # 수도 반경 1 셀은 마을 근처 → 우선순위 2
        village_map[cell] = max(village_map[cell], 2)
    for cell in utils.circle(capital, 2, map_size):  # 반경 2 셀은 외곽 → 우선순위 1
        village_map[cell] = max(village_map[cell], 1)

# 마을 배치가 안 된 0번 셀들을 대상으로 무작위 마을 생성
while 0 in village_map:
    # 아직 배정되지 않은 셀 중 하나를 무작위로 선택
    new_village = random.choice(list(filter(lambda tile: True if village_map[tile] == 0 else False,
                                            list(range(len(village_map))))))
    village_map[new_village] = 3  # 중심 마을로 지정
    for cell in utils.circle(new_village, 1, map_size):  # 반경 1: 마을 인접지
        village_map[cell] = max(village_map[cell], 2)
    for cell in utils.circle(new_village, 2, map_size):  # 반경 2: 마을 외곽지
        village_map[cell] = max(village_map[cell], 1)
    village_count += 1  # 마을 수 증가
    

# 특정 셀에서 자원이 생성될지를 결정하는 함수
def proc(cell_, probability):
    # 마을 반경 2 이내 셀(village_map 값이 2)이 확률에 따라 자원 생성
    # 외곽 지역(값이 1)은 BORDER_EXPANSION을 곱한 낮은 확률로 자원 생성
    return (village_map[cell_] == 2 and random.random() < probability) or\
           (village_map[cell_] == 1 and random.random() < probability * BORDER_EXPANSION)

# 각 셀에 부족 특성과 위치에 따라 자원(resource) 및 마을 설정
for cell in range(map_size**2):
    if world_map[cell]['type'] == 'ground':
        # 해당 부족이 선호하는 fruit, crop 자원의 가중 확률 계산
        fruit = general_probs['fruit'] * terrain_probs['fruit'][world_map[cell]['tribe']]
        crop = general_probs['crop'] * terrain_probs['crop'][world_map[cell]['tribe']]
        if world_map[cell]['above'] != 'capital':
            if village_map[cell] == 3:
                # 마을 중심지에 위치한 경우는 village로 지정
                world_map[cell]['above'] = 'village'
            elif proc(cell, fruit * (1 - crop / 2)):
                # 과일이 상대적으로 우세한 경우
                world_map[cell]['above'] = 'fruit'
            elif proc(cell, crop * (1 - fruit / 2)):
                # 곡물이 우세한 경우
                world_map[cell]['above'] = 'crop'
    elif world_map[cell]['type'] == 'forest':
        if world_map[cell]['above'] != 'capital':
            if village_map[cell] == 3:
                # 숲 위의 마을은 ground로 타입을 바꾸고 village로 설정
                world_map[cell]['type'] = 'ground'
                world_map[cell]['above'] = 'village'
            elif proc(cell, general_probs['game'] * terrain_probs['game'][world_map[cell]['tribe']]):
                # 사냥감 자원 설정
                world_map[cell]['above'] = 'game'
    elif world_map[cell]['type'] == 'water':
        # 물 위에 물고기 자원을 확률적으로 배치
        if proc(cell, general_probs['fish'] * terrain_probs['fish'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'fish'
    elif world_map[cell]['type'] == 'ocean':
        # 바다(ocean) 위에 고래 자원을 확률적으로 배치
        if proc(cell, general_probs['whale'] * terrain_probs['whale'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'whale'
    elif world_map[cell]['type'] == 'mountain':
        # 산 위에 금속 자원을 확률적으로 배치
        if proc(cell, general_probs['metal'] * terrain_probs['metal'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'metal'

# 유적(ruin) 배치 관련 설정
ruins_number = round(map_size**2/40)         # 전체 타일 수의 약 2.5%에 해당하는 유적 수
water_ruins_number = round(ruins_number/3)   # 그중 1/3은 바다 유적
ruins_count = 0
water_ruins_count = 0

# 유적을 지정된 수만큼 배치할 때까지 반복
while ruins_count < ruins_number:
    # 마을이 중심/내곽/외곽이 아닌 곳에만 배치함
    ruin = random.choice(list(filter(lambda tile: True if village_map[tile] in (-1, 0, 1) else False,
                                     list(range(len(village_map))))))
    terrain = world_map[ruin]['type']

    # 물 위가 아니거나, 아직 바다 유적 수가 부족한 경우만 배치
    if terrain != 'water' and (water_ruins_count < water_ruins_number or terrain != 'ocean'):
        world_map[ruin]['above'] = 'ruin'  # 유적 배치 (겹쳐도 표시는 ruin만 함)

        if terrain == 'ocean':
            water_ruins_count += 1  # 바다 유적 카운트 증가

        # 유적 반경 1 셀의 village_map 값을 2로 올림 (내곽으로 표시)
        for cell in utils.circle(ruin, 1, map_size):
            village_map[cell] = max(village_map[cell], 2)

        ruins_count += 1  # 전체 유적 수 증가


# 자원의 개수를 계산하는 함수
def check_resources(resource, capital):
    resources_ = 0
    # 수도 주변 1칸 범위 내에서 해당 자원이 몇 개 있는지 확인
    for neighbour_ in utils.circle(capital, 1, map_size):
        if world_map[neighbour_]['above'] == resource:
            resources_ += 1
    return resources_

# 부족에 맞춰 자원을 배치하는 함수
def post_generate(resource, underneath, quantity, capital):
    resources_ = check_resources(resource, capital)  # 자원의 개수 확인
    # 필요한 자원의 개수가 부족하면 계속해서 자원을 배치
    while resources_ < quantity:
        pos_ = random.randrange(0, 8)  # 자원을 배치할 셀 선택
        territory_ = utils.circle(capital, 1, map_size)  # 수도 주변 1칸 범위 내에서 셀 선택
        # 자원 아래의 타입을 설정 (underneath는 자원이 생성될 셀의 타입)
        world_map[territory_[pos_]]['type'] = underneath
        world_map[territory_[pos_]]['above'] = resource  # 해당 셀에 자원 배치

        # 해당 셀의 주변 이웃이 바다일 경우 물로 변경
        for neighbour_ in utils.plus_sign(territory[pos_], map_size):
            if world_map[neighbour_]['type'] == 'ocean':
                world_map[neighbour_]['type'] = 'water'

        resources_ = check_resources(resource, capital)  # 자원 개수 갱신

# 부족별로 특화된 자원을 배치
for capital in capital_cells:
    if world_map[capital]['tribe'] == 'Imperius':
        post_generate('fruit', 'ground', 2, capital)  # Imperius 부족은 fruit 자원 배치
    elif world_map[capital]['tribe'] == 'Bardur':
        post_generate('game', 'forest', 2, capital)  # Bardur 부족은 game 자원 배치
    elif world_map[capital]['tribe'] == 'Kickoo':
        resources = check_resources('fish', capital)
        # Kickoo 부족은 물고기 자원을 최소 2개 배치하도록 보장
        while resources < 2:
            pos = random.randrange(0, 4)
            territory = utils.plus_sign(capital, map_size)
            world_map[territory[pos]]['type'] = 'water'
            world_map[territory[pos]]['above'] = 'fish'  # 물고기 자원 배치
            # 주변이 물인 경우 바다로 변경 (이중으로 물로 설정)
            for neighbour in utils.plus_sign(territory[pos], map_size):
                if world_map[neighbour]['type'] == 'water':
                    world_map[neighbour]['type'] = 'ocean'
                    for double_neighbour in utils.plus_sign(neighbour, map_size):
                        if world_map[double_neighbour]['type'] != 'water' and world_map[double_neighbour]['type'] != 'ocean':
                            world_map[neighbour]['type'] = 'water'
                            break
            resources = check_resources('fish', capital)  # 자원 개수 다시 체크
        break  # Kickoo 부족만 처리하고 종료 (다른 부족들은 처리하지 않음)
    elif world_map[capital]['tribe'] == 'Zebasi':
        post_generate('crop', 'ground', 1, capital)  # Zebasi 부족은 crop 자원 배치
    elif world_map[capital]['tribe'] == 'Elyrion':
        post_generate('game', 'forest', 2, capital)  # Elyrion 부족은 game 자원 배치
    elif world_map[capital]['tribe'] == 'Polaris':
        # Polaris 부족은 그 주변 셀들을 모두 Polaris로 설정
        for neighbour in utils.circle(capital, 1, map_size):
            world_map[neighbour]['tribe'] = 'Polaris'


# optional display, set up as you want
# for c in range(map_size ** 2):
#     if c % map_size == 0:
#         print()
#     if world_map[c]['above'] == 'capital':
#         print('0', end='')
#         continue
#     if world_map[c]['above'] == 'village':
#         print('v', end='')
#         continue
#     if world_map[c]['above'] == 'ruin':
#         print('r', end='')
#         continue
#     if world_map[c]['type'] == 'ocean':
#         print('o', end='')
#         continue
#     if world_map[c]['type'] == 'ground':
#         print('g', end='')
#         continue
#     if world_map[c]['type'] == 'forest':
#         print('f', end='')
#         continue
#     if world_map[c]['type'] == 'mountain':
#         print('m', end='')
#         continue
#     if world_map[c]['type'] == 'water':
#         print('w', end='')
#         continue


def generate_map(world_map, map_size, initial_land, smoothing, relief, tribes):
    # 맵 초기화: ocean으로 설정
    j = 0
    while j < map_size ** 2 * initial_land:
        cell = random.randrange(0, map_size ** 2)
        if world_map[cell]['type'] == 'ocean':
            j += 1
            world_map[cell]['type'] = 'ground'

    land_coefficient = (0.5 + relief) / 9

    # 지형 스무딩
    for i in range(smoothing):
        for cell in range(map_size ** 2):
            water_count = 0
            tile_count = 0
            neighbours = utils.round_(cell, 1, map_size)
            for i in range(len(neighbours)):
                if world_map[neighbours[i]]['type'] == 'ocean':
                    water_count += 1
                tile_count += 1
            if water_count / tile_count <= land_coefficient:
                world_map[cell]['road'] = True

        for cell in range(map_size ** 2):
            if world_map[cell]['road']:
                world_map[cell]['road'] = False
                world_map[cell]['type'] = 'ground'
            else:
                world_map[cell]['type'] = 'ocean'

    # 수도 셀 배치
    capital_cells = []
    capital_map = {}
    for tribe in tribes:
        for row in range(2, map_size - 2):
            for column in range(2, map_size - 2):
                if world_map[row * map_size + column]['type'] == 'ground':
                    capital_map[row * map_size + column] = 0
    for tribe in tribes:
        max_ = 0
        for cell in capital_map:
            capital_map[cell] = map_size
            for capital_cell in capital_cells:
                capital_map[cell] = min(capital_map[cell], utils.distance(cell, capital_cell, map_size))
            max_ = max(max_, capital_map[cell])

        len_ = 0
        for cell in capital_map:
            if capital_map[cell] == max_:
                len_ += 1
        rand_cell = random.randrange(0, len_)
        for cell in capital_map.items():
            if cell[1] == max_:
                if rand_cell == 0:
                    capital_cells.append(int(cell[0]))
                rand_cell -= 1

    # 수도 셀에 'capital' 표시
    for i in range(len(capital_cells)):
        world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['above'] = 'capital'
        world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['tribe'] = tribes[i]

    return world_map
