import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QFormLayout,
    QScrollArea, QFrame, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer

import app  # app.create_full_map 을 사용합니다.

class MapCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # 부모(MapViewer)에서 아래 속성들을 복사해줘야 합니다:
        # self.world_map, self.map_size, self.tile_w,
        # self.terrain_pixmaps, self.head_pixmaps,
        # self.resource_pixmaps, self.tribe_specific_resource_pixmaps,
        # 그리고 self.orig_dims (원본 에셋 크기)
        self.offset_x = 0
        self.offset_y = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)

        if not self.world_map or self.map_size == 0:
            return

        # 1) 캔버스 크기 (MapCanvas 위젯 자체 크기)
        canvas_w = self.width()
        canvas_h = self.height()

        # 1.5) 타일 폭/높이 계산
        tw = self.tile_w
        # orig_dims 에서 임의로 'Xin-xi'의 ground 크기 가져와서 스케일 높이 계산
        orig_w, orig_h = self.orig_dims['Xin-xi']['ground']
        tile_h = orig_h * tw / orig_w

        # 2) 맵 전체 예상 크기
        map_w = self.map_size * tw
        map_h = self.map_size * tile_h

        # 3) 캔버스 중앙에 (0,0) 타일 꼭짓점이 오도록 배치
        panel_w = self.parent().controls_frame.width()
        iso_map_w = (self.map_size - 1) * (tw / 2) + tw
        origin_x = panel_w + ((canvas_w - panel_w - iso_map_w) // 2) + self.offset_x
        origin_y = max(0, (canvas_h - map_h) // 2) + self.offset_y

        # 6) 한 레이어로만 그리기 (HTML index.js 로직 동일하게)
        # ── 6) 셀 그리기 (단일 레이어) ─────────────────────
        for idx, cell in enumerate(self.world_map):
            row = idx // self.map_size
            col = idx % self.map_size

            # 1) 이소메트릭 좌표
            dx = (col - row) * (tw / 2)
            dy = (col + row) * (tile_h * 606 / 1908)
            x = int(origin_x + dx)
            y = int(origin_y + dy)

            # 2) 한 장의 타일 이미지만 선택해서 그리기
            tribe = cell['tribe']
            ctype = cell['type']
            terrain_pm = self.terrain_pixmaps.get(tribe, {}).get(ctype)
            if not terrain_pm or terrain_pm.isNull():
                terrain_pm = self.terrain_pixmaps.get(tribe, {}).get('ground')
            if not terrain_pm or terrain_pm.isNull():
                terrain_pm = self.terrain_pixmaps['Xin-xi']['ground']
            painter.drawPixmap(x, y, terrain_pm)

            # 3) 수도 / 공용 자원 / 부족 특화 자원 그리기
            above = cell.get('above')
            if above == 'capital':
                head_pm = self.head_pixmaps.get(cell['tribe'])
                if head_pm and not head_pm.isNull():
                    painter.drawPixmap(x, y - int(head_pm.height() * 0.35), head_pm)
            elif above in self.resource_pixmaps:
                res_pm = self.resource_pixmaps[above]
                if res_pm and not res_pm.isNull():
                    painter.drawPixmap(x, y - int(res_pm.height() * 0.15), res_pm)
            else:
                spec_pm = self.tribe_specific_resource_pixmaps[cell['tribe']].get(above)
                if spec_pm and not spec_pm.isNull():
                    painter.drawPixmap(x, y - int(spec_pm.height() * 0.15), spec_pm)

            if ctype not in ('ground', 'forest', 'mountain', 'ocean', 'water'):
                print(f"경고: 알 수 없는 type 발견! tribe={tribe}, type={ctype}, idx={idx}")


class MapViewer(QWidget):
    
    def resizeEvent(self, event):
        # 컨트롤 패널 너비를 구해서 캔버스 최대 너비를 설정
        cw = self.controls_frame.width()
        self.canvas.setMaximumWidth(self.width() - cw)
        # 기본 동작 유지
        return super().resizeEvent(event)   
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polytopia Map Viewer (PyQt5)")

        # --- 위치 오프셋 ---
        self.offset_x = 0
        self.offset_y = 0

        # --- assets 폴더 경로 및 타일 크기 ---
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        self.tile_w = 64

        # --- pixmap 캐시 초기화 ---
        # terrain_pixmaps, head_pixmaps, resource_pixmaps, tribe_specific_resource_pixmaps,
        # 그리고 원본 크기를 저장할 orig_dims 를 세팅합니다.
        self.load_pixmaps()

        # --- 맵 데이터 초기값 ---
        self.world_map = []
        self.map_size = 16

        # --- UI 구성 ---
        self.init_ui()

        # --- 첫 맵 생성 ---
        self.on_generate()

    def load_pixmaps(self):
        # 초기화
        self.terrain_pixmaps = {}
        self.head_pixmaps = {}
        self.resource_pixmaps = {}
        self.tribe_specific_resource_pixmaps = {}
        self.orig_dims = {}

        for tribe in app.tribes_list:
            self.terrain_pixmaps[tribe] = {}
            self.orig_dims[tribe] = {}
            self.tribe_specific_resource_pixmaps[tribe] = {}

        # 1) 공통 지형 (ocean, water) 로드
        for ttype in ('ocean', 'water'):
            path = os.path.join(self.assets_dir, f"{ttype}.png")
            orig = QPixmap(path)
            if orig.isNull():
                print(f"경고: 공통 지형 이미지 로드 실패: {path}")
                continue
            ow, oh = orig.width(), orig.height()
            pm = orig.scaled(
                self.tile_w,
                int(self.tile_w * oh / ow),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            for tribe in app.tribes_list:
                self.terrain_pixmaps[tribe][ttype] = pm
                self.orig_dims[tribe][ttype] = (ow, oh)

        # 2) 부족별 기본 지형 (ground, forest, mountain) 로드
        for tribe in app.tribes_list:
            for biome in ('ground', 'forest', 'mountain'):
                path = os.path.join(self.assets_dir, tribe, f"{tribe} {biome}.png")
                orig = QPixmap(path)
                if orig.isNull():
                    print(f"경고: {tribe} {biome} 이미지 로드 실패: {path}")
                    continue
                ow, oh = orig.width(), orig.height()
                pm = orig.scaled(
                    self.tile_w,
                    int(self.tile_w * oh / ow),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.terrain_pixmaps[tribe][biome] = pm
                self.orig_dims[tribe][biome] = (ow, oh)

        # 3) forest/mountain 은 ground 위에 합성해서 투명 블록 문제 해결
        for tribe in app.tribes_list:
            ground_pm = self.terrain_pixmaps[tribe].get('ground')
            if not ground_pm:
                continue
            gw, gh = ground_pm.width(), ground_pm.height()
            for biome in ('forest', 'mountain'):
                overlay_pm = self.terrain_pixmaps[tribe].get(biome)
                if not overlay_pm:
                    continue
                ow, oh = overlay_pm.width(), overlay_pm.height()

                # 빈 투명 Pixmap 생성
                composite = QPixmap(gw, gh)
                composite.fill(Qt.transparent)
                p = QPainter(composite)

                # ① ground 그리기
                p.drawPixmap(0, 0, ground_pm)

                # ② overlay 그리기
                if biome == 'mountain':
                    offset = oh // 2
                else:
                    offset = int(oh * 0.35)
                # ground 바닥에서 위로 offset 만큼
                y = gh - oh - offset
                p.drawPixmap(0, y, overlay_pm)

                p.end()

                # 덮어쓰기
                self.terrain_pixmaps[tribe][biome] = composite

        # (이하 head, resource, tribe-specific resource 로드 로직 그대로 유지)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        # 왼쪽 컨트롤
        self.controls_frame = QFrame()
        self.controls_frame.setFrameShape(QFrame.StyledPanel)
        self.controls_frame.setMaximumWidth(350)
        ctr = QVBoxLayout(self.controls_frame)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_w = QWidget()
        form = QFormLayout(form_w)

        self.map_size_input = QSpinBox();    self.map_size_input.setRange(5,50);    self.map_size_input.setValue(16)
        self.initial_land_input = QDoubleSpinBox(); self.initial_land_input.setRange(0.0,1.0); self.initial_land_input.setSingleStep(0.01); self.initial_land_input.setValue(0.5)
        self.smoothing_input = QSpinBox();     self.smoothing_input.setRange(0,10);     self.smoothing_input.setValue(3)
        self.relief_input = QSpinBox();        self.relief_input.setRange(1,8);       self.relief_input.setValue(4)
        self.tribes_input = QLineEdit("Kickoo Hoodrick Vengir Zebasi Ai-mo Polaris")
        self.fill_tribe_input = QLineEdit()
        self.no_biomes_checkbox = QCheckBox("Don't generate biomes")
        self.no_resources_checkbox = QCheckBox("Don't generate resources")

        form.addRow("Map Size:", self.map_size_input)
        form.addRow("Initial Land:", self.initial_land_input)
        form.addRow("Smoothing:", self.smoothing_input)
        form.addRow("Relief:", self.relief_input)
        form.addRow("Tribes:", self.tribes_input)
        form.addRow("Fill Tribe:", self.fill_tribe_input)
        form.addRow(self.no_biomes_checkbox)
        form.addRow(self.no_resources_checkbox)

        scroll.setWidget(form_w)
        ctr.addWidget(scroll)

        # --- 방향키 버튼 추가 (리모컨 스타일) ---
        grid = QGridLayout()
        self.btn_up = QPushButton('↑')
        self.btn_down = QPushButton('↓')
        self.btn_left = QPushButton('←')
        self.btn_right = QPushButton('→')
        self.btn_ok = QPushButton('ㅇ')
        self.btn_ok.setEnabled(False)  # 기능 없음
        grid.addWidget(self.btn_up,    0, 1)
        grid.addWidget(self.btn_left,  1, 0)  # ← 는 왼쪽
        grid.addWidget(self.btn_ok,    1, 1)
        grid.addWidget(self.btn_right, 1, 2)  # → 는 오른쪽
        grid.addWidget(self.btn_down,  2, 1)
        ctr.addLayout(grid)

        # --- 줌 인/아웃 버튼 추가 ---
        zoom_layout = QHBoxLayout()
        self.btn_zoom_in = QPushButton('+')
        self.btn_zoom_out = QPushButton('-')
        zoom_layout.addWidget(self.btn_zoom_in)
        zoom_layout.addWidget(self.btn_zoom_out)
        ctr.addLayout(zoom_layout)

        # 타이머 4개 (역할도 바꿔야 함)
        self.tmr_up = QTimer(self)
        self.tmr_down = QTimer(self)
        self.tmr_left = QTimer(self)
        self.tmr_right = QTimer(self)
        self.tmr_up.setInterval(200)
        self.tmr_down.setInterval(200)
        self.tmr_left.setInterval(200)
        self.tmr_right.setInterval(200)
        self.tmr_up.timeout.connect(lambda: self.move_map(0, 10))
        self.tmr_down.timeout.connect(lambda: self.move_map(0, -10))
        self.tmr_left.timeout.connect(lambda: self.move_map(10, 0))
        self.tmr_right.timeout.connect(lambda: self.move_map(-10, 0))

        self.btn_up.pressed.connect(lambda: self.tmr_up.start())
        self.btn_up.released.connect(lambda: self.tmr_up.stop())
        self.btn_down.pressed.connect(lambda: self.tmr_down.start())
        self.btn_down.released.connect(lambda: self.tmr_down.stop())
        self.btn_left.pressed.connect(lambda: self.tmr_left.start())
        self.btn_left.released.connect(lambda: self.tmr_left.stop())
        self.btn_right.pressed.connect(lambda: self.tmr_right.start())
        self.btn_right.released.connect(lambda: self.tmr_right.stop())

        # 단일 클릭도 역할 바꿔서 연결
        self.btn_up.clicked.connect(lambda: self.move_map(0, 10))
        self.btn_down.clicked.connect(lambda: self.move_map(0, -10))
        self.btn_left.clicked.connect(lambda: self.move_map(10, 0))
        self.btn_right.clicked.connect(lambda: self.move_map(-10, 0))

        # 줌 인/아웃 기능 연결
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        self.btn_zoom_out.clicked.connect(self.zoom_out)

        btn = QPushButton("Generate Map")
        btn.clicked.connect(self.on_generate)
        ctr.addWidget(btn)

        main_layout.addWidget(self.controls_frame)

        # 오른쪽은 MapCanvas
        self.canvas = MapCanvas(self)
        # 캔버스에 필요한 속성 복사
        for attr in (
            'tile_w', 'terrain_pixmaps', 'head_pixmaps',
            'resource_pixmaps', 'tribe_specific_resource_pixmaps',
            'orig_dims', 'world_map', 'map_size'
        ):
            setattr(self.canvas, attr, getattr(self, attr))
        # 오프셋도 복사
        self.canvas.offset_x = self.offset_x
        self.canvas.offset_y = self.offset_y
        # 수정: stretch=1을 주면, 남은 공간(=전체 창 – 패널 너비)을 캔버스가 자동으로 채웁니다.
        main_layout.addWidget(self.canvas, 1)

    def on_generate(self):
        size = self.map_size_input.value()
        land = self.initial_land_input.value()
        smooth = self.smoothing_input.value()
        relief = self.relief_input.value()
        tribes = [t for t in self.tribes_input.text().split() if t in app.tribes_list] or ['Kickoo']
        fill = self.fill_tribe_input.text() or None
        no_biomes = self.no_biomes_checkbox.isChecked()
        no_resources = self.no_resources_checkbox.isChecked()

        self.map_size = size
        self.world_map = app.create_full_map(
            map_size=size,
            initial_land=land,
            smoothing=smooth,
            relief=relief,
            tribes_param=tribes,
            fill_tribe=fill,
            no_biomes=no_biomes,
            no_resources=no_resources
        )

        # 캔버스에 맵 갱신
        self.canvas.world_map = self.world_map
        self.canvas.map_size = self.map_size
        self.canvas.update()

    def move_map(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.canvas.offset_x = self.offset_x
        self.canvas.offset_y = self.offset_y
        self.canvas.update()

    def zoom_in(self):
        self.tile_w = min(256, self.tile_w + 8)
        self.canvas.tile_w = self.tile_w
        self.load_pixmaps()
        self.canvas.terrain_pixmaps = self.terrain_pixmaps
        self.canvas.head_pixmaps = self.head_pixmaps
        self.canvas.resource_pixmaps = self.resource_pixmaps
        self.canvas.tribe_specific_resource_pixmaps = self.tribe_specific_resource_pixmaps
        self.canvas.orig_dims = self.orig_dims
        self.canvas.update()

    def zoom_out(self):
        self.tile_w = max(16, self.tile_w - 8)
        self.canvas.tile_w = self.tile_w
        self.load_pixmaps()
        self.canvas.terrain_pixmaps = self.terrain_pixmaps
        self.canvas.head_pixmaps = self.head_pixmaps
        self.canvas.resource_pixmaps = self.resource_pixmaps
        self.canvas.tribe_specific_resource_pixmaps = self.tribe_specific_resource_pixmaps
        self.canvas.orig_dims = self.orig_dims
        self.canvas.update()

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.resize(1280, 720)
    viewer.show()
    sys.exit(app_qt.exec_())
