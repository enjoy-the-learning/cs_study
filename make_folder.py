import os

# 원하는 디렉토리명 지정하기
root_dir = "coffeeisnak"

# 생성할 서브디렉토리 목록 지정하기
subdirs = [
    "os",
    "algorithm",
    "data_structure",
    "clouds",
    "virtualization",
    "security",
    "network",
    "databases",
    "computer_architecture",
    "data_analysis",
    "languages",
    "sw_engineering",
    "data_stacks"
]

# 루트 디렉토리를 생성
os.makedirs(root_dir, exist_ok=True)
print(f"Root directory '{root_dir}' created (if it didn't already exist).")

# 각 서브디렉토리 생성과 .gitkeep 파일 생성
for subdir in subdirs:
    dir_path = os.path.join(root_dir, subdir)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Subdirectory '{dir_path}' created.")

    # .gitkeep 파일 생성
    gitkeep_path = os.path.join(dir_path, ".gitkeep")
    with open(gitkeep_path, "w") as f:
        pass  # 빈 파일 생성
    print(f"'.gitkeep' file created in '{dir_path}'.")

print("\n✅ All directories and .gitkeep files have been created!")
