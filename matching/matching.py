import argparse
from collections import defaultdict

import csv

def test_case():
    # 講師情報
    teachers_info = {
        "T001": {
            "subjects": ["Math", "English"],
            "assigned_students": ["S001"]
        },
        "T002": {
            "subjects": ["English"],
            "assigned_students": ["S002"]
        },
        "T003": {
            "subjects": ["Math"],
            "assigned_students": ["S003"]
        }
    }

    # 講師スロット
    teachers_slots = defaultdict(list, {
        "T001": [("0801A", 1), ("0801B", 1)],
        "T002": [("0801B", 1), ("0802A", 1)],
        "T003": [("0802B", 1)]
    })

    # 生徒情報
    students_info = {
        "S001": {
            "demand": {"Math": 1, "English": 1}
        },
        "S002": {
            "demand": {"English": 1}
        },
        "S003": {
            "demand": {"Math": 2}
        }
    }

    # 生徒スロット
    students_slots = defaultdict(list, {
        "S001": ["0801A", "0801B"],
        "S002": ["0801B"],
        "S003": ["0802A", "0802B"]
    })

    return teachers_info, teachers_slots, students_info, students_slots

def read_csv():
    # ==== 講師情報（固定情報 + スロット） ====
    teachers_info = {}      # 固定情報（subjects, assigned_students）
    teachers_slots = defaultdict(list)  # 講師ID -> スロットリスト（slot, k）

    # teachers_info.csv 読み込み
    with open("teachers_info.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t_id = row["teacher_id"]
            teachers_info[t_id] = {
                "subjects": row["subjects"].split("|"),
                "assigned_students": row["assigned_students"].split("|") if row["assigned_students"] else []
            }

    # teachers_slot.csv 読み込み
    with open("teachers_slot.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t_id = row["teacher_id"]
            slot = row["slot"]
            available = int(row["available"])
            for k in range(available):  # 1コマに対して k 枠作成
                teachers_slots[t_id].append((slot, k))


    # ==== 生徒情報（固定情報 + スロット） ====
    students_info = {}       # 固定情報（demand）
    students_slots = defaultdict(list)  # 生徒ID -> 希望スロットリスト

    # students_info.csv 読み込み
    with open("students_info.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row["student_id"]
            subject = row["subject"]
            classes = int(row["classes"])
            if s_id not in students_info:
                students_info[s_id] = {"demand": {}}
            students_info[s_id]["demand"][subject] = classes

    # students_slot.csv 読み込み（縦並び形式）
    with open("students_slot.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row["student_id"]
            slot = row["slot"]
            students_slots[s_id].append(slot)
    
    return teachers_info, teachers_slots, students_info, students_slots


def run(teachers_info, teachers_slots, students_info, students_slots):
    # ==== マッチング用グラフ構築 ====   
    # 生徒の「希望科目数分のダミーノード」を作る
    student_nodes = []
    for s_id, info in students_info.items():
        demand = info["demand"]
        for subject, count in demand.items():
            for i in range(count):
                student_nodes.append((s_id, subject, i))

    print(student_nodes)

    # 生徒ごとの担当講師辞書
    student2teachers = defaultdict(set)
    for t_id, t_info in teachers_info.items():
        for s_id in t_info["assigned_students"]:
            student2teachers[s_id].add(t_id)

    print(student2teachers)

    # グラフ (生徒ノード -> 講師枠ノード)
    edges = defaultdict(list)
    for s_id, subject, i in student_nodes:
        preferred_slots = students_slots[s_id]  # 生徒の希望スロットリスト

        priority_edges = []  # 担当講師
        normal_edges = []    # 非担当講師

        for t_id, slots in teachers_slots.items():  # 講師ごとのスロットリスト
            t_subjects = teachers_info[t_id]["subjects"]  # 講師が教えられる科目

            if subject not in t_subjects:
                continue  # 教えられない科目はスキップ

            for slot, k in slots:
                if slot not in preferred_slots:
                    continue  # 生徒が希望していないスロットはスキップ

                # 担当講師なら先頭、そうでなければ後ろに追加
                if t_id in student2teachers[s_id]:
                    priority_edges.append((t_id, slot, k))
                else:
                    normal_edges.append((t_id, slot, k))

        # k の大きい順にソート（担当講師と非担当講師ごとに）
        priority_edges.sort(key=lambda x: -x[2])
        normal_edges.sort(key=lambda x: -x[2])

        # edges に結合
        edges[(s_id, subject, i)] = priority_edges + normal_edges

    print(edges)
    
    # ==== DFSベースの最大マッチング ====

    match_to = {}  # 講師枠 -> 生徒ノード

    # tnode の残り枠 k を管理
    slot_remaining = defaultdict(int)
    for t_id, slots in teachers_slots.items():
        for slot, k in slots:
            slot_remaining[(t_id, slot, k)] += 1

    # 生徒ごとの使用スロット
    student_used_slots = {s_id: set() for s_id in students_info.keys()}

    def _dfs(snode, visited):
        s_id, subject, _ = snode
        for tnode in edges[snode]:
            t_id, slot, k = tnode
            if tnode in visited:
                continue
            if slot in student_used_slots[s_id]:
                continue  # 同じスロットは使えない
            if slot_remaining[tnode] <= 0:
                continue  # 残り 枠 がない

            visited.add(tnode)

            if tnode not in match_to:
                # 空きがある場合
                match_to[tnode] = snode
                slot_remaining[tnode] -= 1
                student_used_slots[s_id].add(slot)
                return True
            else:
                # 再帰的に置き換え可能かチェック
                prev_snode = match_to[tnode]
                if _dfs(prev_snode, visited):
                    match_to[tnode] = snode
                    # 残り枠は減らさず、使用スロットは更新
                    student_used_slots[s_id].add(slot)
                    return True
        return False

    for snode in student_nodes:
        _dfs(snode, set())

    # ==== マッチング済みの結果出力 ====
    assigned_students = defaultdict(list)  # s_id -> list of subject, slot
    assigned_teachers = defaultdict(lambda: defaultdict(int)) 
    assignments = []

    for tnode, snode in match_to.items():
        t_id, slot, k = tnode
        s_id, subject, i = snode

        # 生徒ノードに割り当てられたスロット記録
        assigned_students[s_id].append((subject, slot))

        # 講師の枠ごとの使用済み件数記録
        assigned_teachers[t_id][slot] += 1
        
        assignments.append({
            "student_id": s_id,
            "subject": subject,
            "teacher_id": t_id,
            "slot": slot
        })
    
    # ==== 生徒ノード未割当と空きスロットを同時に計算 ====
    unmatched_students = defaultdict(lambda: defaultdict(int))
    unmatched_student_slots = []
    unmatched_students_list = []

    for s_id, info in students_info.items():
        demand = info["demand"]
        # 各科目ごとに
        for subject, count in demand.items():
            for i in range(count):
                snode = (s_id, subject, i)
                # edges にあるノードが match_to になければ未割当
                if all(match_to.get(tnode) != snode for tnode in edges[snode]):
                    unmatched_students[s_id][subject] += 1
        
        # unmatched_students に入れた内容をリスト化（←これで CSV 出力用）
        for subject, remaining in unmatched_students[s_id].items():
            unmatched_students_list.append({
                "student_id": s_id,
                "subject": subject,
                "classes": remaining
            })
            
        # 空きスロット
        used_slots = [slot for _, slot in assigned_students.get(s_id, [])]
        for slot in students_slots[s_id]:
            if slot not in used_slots:
                unmatched_student_slots.append({
                    "student_id": s_id,
                    "slot": slot
                })
    
    # ==== 講師の空きスロット ====
    unmatched_teacher_slots = []

    for t_id, slots in teachers_slots.items():
        # slot ごとの最大 k を辞書にまとめる
        slot_max = {}
        for slot, k in slots:
            slot_max[slot] = max(slot_max.get(slot, 0), k+1)

        # 残っている k を CSV 用リストに追加
        for slot, max_k in slot_max.items():
            used = assigned_teachers[t_id].get(slot, 0)
            remaining = max_k - used
            if  remaining > 0:
                unmatched_teacher_slots.append({
                    "teacher_id": t_id,
                    "slot": slot,
                    "rest": remaining
                })

    # ==== CSV 出力 ====
    for filename, fieldnames, data in [
        ("assignments.csv", ["student_id","subject","teacher_id","slot"], assignments),
        ("remain_students_demand.csv", ["student_id","subject","classes"], unmatched_students_list),
        ("remain_students_slot.csv", ["student_id","slot"], unmatched_student_slots),
        ("remain_teachers_slot.csv", ["teacher_id","slot","rest"], unmatched_teacher_slots)
    ]:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # ==== マッチングできなかった生徒ノードを CSV 出力 ====
    unmatched_students = defaultdict(lambda: defaultdict(int))

    for snode in student_nodes:
        if all(match_to.get(tnode) != snode for tnode in edges[snode]):
            s_id, subject, i = snode
            unmatched_students[s_id][subject] += 1  # 残りコマ数をカウント

    with open("remain_students_demand.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["student_id", "subject", "classes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s_id, subjects in unmatched_students.items():
            for subject, remaining in subjects.items():
                writer.writerow({
                    "student_id": s_id,
                    "subject": subject,
                    "classes": remaining
                })

    return assignments


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--t",
        action="store_true",
        help="テストケースを使用する場合は指定"
    )
    args = parser.parse_args()

    # csv入力
    if not args.t:
        teachers_info, teachers_slots, students_info, students_slots = read_csv()
    else:
        teachers_info, teachers_slots, students_info, students_slots = test_case()

    # マッチング
    assignments = run(teachers_info, teachers_slots, students_info, students_slots)

    # 表示
    for row in assignments:
        print(row)