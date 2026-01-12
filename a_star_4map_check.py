# a_star_4map_check.py
# 4分割Map配送がA*で解けるかの健全性確認コード
# コピペ即実行用

import heapq

# -------------------------
# Map 定義（8x8 × 4）
# -------------------------
Map1 = [
    "■■■Ｂ・・▲▲",
    "■■■■◯・▲▲",
    "■■■■・・▲▲",
    "■■■■・・②＃",
    "■■■■・・＃＃",
    "■■■■・・▲▲",
    "・・◯・・・▲▲",
    "・・・・・・▲▲",
]

Map2 = [
    "▲▲・・Ａ■■■",
    "▲▲・・■■■■",
    "▲▲・◯■■■■",
    "＃＃・・■■■■",
    "＃②・・■■■■",
    "▲▲・・■■■■",
    "▲▲・・・・・・",
    "▲▲・・・・・・",
]

Map3 = [
    "▲＃①▲▲▲▲▲",
    "▲＃＃▲▲▲▲▲",
    "▲＃＃▲▲▲▲▲",
    "▲①＃▲▲▲▲▲",
    "・・・・・・▲▲",
    "・・・・◯・▲▲",
    "■Ｃ■■・・②＃",
    "■■■■・・＃＃",
]

Map4 = [
    "▲▲▲▲▲＃①▲",
    "▲▲▲▲▲＃＃▲",
    "▲▲▲▲▲＃＃▲",
    "▲▲▲▲▲①＃▲",
    "▲▲・・・◯・・",
    "▲▲・・・・・・",
    "＃＃・・受■■■",
    "＃②・・■■■■",
]

# -------------------------
# 16x16 結合
# -------------------------
def merge_maps(m1, m2, m3, m4):
    grid = []
    for y in range(8):
        grid.append(list(m1[y] + m2[y]))
    for y in range(8):
        grid.append(list(m3[y] + m4[y]))
    return grid

grid = merge_maps(Map1, Map2, Map3, Map4)

H, W = 16, 16

# -------------------------
# 探索設定
# -------------------------
MOVE_COST = {
    "・": 1,
    "＃": 0.5,
    "▲": 5,
    "◯": 10,
    "①": 1,
    "②": 1,
    "Ａ": 0,
    "Ｂ": 0,
    "Ｃ": 0,
    "受": 0,
}

BLOCK = {"■"}

# -------------------------
# スタート・ゴール探索
# -------------------------
for y in range(H):
    for x in range(W):
        if grid[y][x] == "受":
            start = (x, y)
        if grid[y][x] == "Ａ":
            goal = (x, y)

# -------------------------
# A* 実装
# -------------------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            cell = grid[ny][nx]
            if cell in BLOCK:
                continue

            new_cost = cost_so_far[current] + MOVE_COST.get(cell, 1)
            if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                cost_so_far[(nx, ny)] = new_cost
                priority = new_cost + heuristic((nx, ny), goal)
                heapq.heappush(pq, (priority, (nx, ny)))
                came_from[(nx, ny)] = current

    # 経路復元
    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = came_from.get(cur)
    path.reverse()
    return path, cost_so_far.get(goal, None)

path, cost = astar(grid, start, goal)

# -------------------------
# 結果表示
# -------------------------
print("Start:", start)
print("Goal :", goal)
print("Total cost:", cost)
print("Path length:", len(path))

view = [row.copy() for row in grid]
for x, y in path:
    if view[y][x] == "・":
        view[y][x] = "★"

print("\n--- Path Map ---")
for row in view:
    print("".join(row))