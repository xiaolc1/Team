def count_filtered_communities(filename, min_size, max_size, output_filename):
    # 初始化计数器
    num_filtered_communities = 0
    # 打开输出文件进行写入
    with open(output_filename, 'w') as output_file:
        # 打开输入文件并逐行读取数据
        with open(filename, 'r') as file:
            current_community = None
            team_members = []

            for line in file:
                line = line.strip()

                if line.startswith('Community'):
                    # 如果遇到社区信息行，则处理上一个社区的成员列表
                    if current_community is not None and team_members:
                        team_size = len(team_members)
                        if min_size <= team_size <= max_size:
                            num_filtered_communities += 1
                            # 写入社区信息和成员到输出文件
                            output_file.write(f"Community {current_community}:\n")
                            for member in team_members:
                                output_file.write(f"{member}\n")
                            output_file.write("\n")  # 添加空行分隔不同社区

                        team_members = []  # 重置成员列表

                    # 更新当前社区信息
                    current_community = line.split()[1][:-1]

                else:
                    # 如果不是社区信息行，则将成员添加到成员列表中
                    team_members.append(line)

            # 处理最后一个社区的成员列表
            if current_community is not None and team_members:
                team_size = len(team_members)
                if min_size <= team_size <= max_size:
                    num_filtered_communities += 1
                    # 写入最后一个社区信息和成员到输出文件
                    output_file.write(f"Community {current_community}:\n")
                    for member in team_members:
                        output_file.write(f"{member}\n")
                    output_file.write("\n")  # 添加空行分隔不同社区

    return num_filtered_communities


# 指定输入文件名和输出文件名
input_filename = '../../team_predict/AMiner/data_process/communities.txt'
output_filename = '../../team_predict/AMiner/communities_2-10.txt'
min_team_size = 2
max_team_size = 10

# 统计团队人数在指定范围内的社区的数量
num_filtered_communities = count_filtered_communities(input_filename, min_team_size, max_team_size, output_filename)

# 输出符合条件的社区数量
print(f"Number of communities with {min_team_size}-{max_team_size} members: {num_filtered_communities}")
