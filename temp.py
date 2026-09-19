from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
print(SCRIPT_DIR)




# for d in [19, 20]:
#     # print('hello')
#     for h in range(14, 26):
#         print(f"day: {d},  hour:{h},  index {h - 14 + ((d - 19) * 12)}")
#         # print('hi')

# for h in range(14, 26):
#     # print(f"day: {d},  hour:{h}, index {(h - 13) * ((d - 19) * 12)}"))
#     print(h)
# x = ['2026-09-19 15:00:00', '2026-09-19 19:58:00', '2026-09-20 19:55:00',  '2026-09-20 01:59:00', '2026-09-20 00:59:00', '2026-09-19 14:00:00', '2026-09-19 23:59:00', '2026-09-21 00:59:00', '2026-09-21 01:59:00', '2026-09-19 23:59:00', '2026-09-19 23:40:00', '2026-09-19 23:30:00', '2026-09-19 23:00:00']
# r = [0] * 24
# for s in x:

#     a = int(s.split(' ')[1].split(':')[0])
#     if a > 1:
#         a -= 14
#     else:
#         a -= 2
#     b = (int(s.split(' ')[0].split('-')[2])-19) * 12

#     print(f"{s}:  {a} + {b} = {a + b}")
#     r[a + ((int(s.split(' ')[0].split('-')[2]) - 19) * 12)] += 1
# print(f"{r}")