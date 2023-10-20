import itertools
import os


def similarity_percentage(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        content1, content2 = f1.read(), f2.read()
        common_length = sum(b1 == b2 for b1, b2 in zip(content1, content2))

        if len(content2) == 0 and len(content1) == 0:
            return True

        return 100 * common_length / max(len(content1), len(content2))


def relative_path_resolve(file):
    relative_path = os.path.relpath(file)
    return relative_path[relative_path.index("/") + 1::]


def main(directory1, directory2, similarity_threshold):
    dir1_files = list(map(lambda t: os.path.join(directory1, t), os.listdir(directory1)))
    dir2_files = list(map(lambda t: os.path.join(directory2, t), os.listdir(directory2)))

    identical, similar = set(), set()
    for file1, file2 in itertools.product(dir1_files, dir2_files):
        percentage = similarity_percentage(file1, file2)

        if abs(percentage - 100) < 1e-10:
            identical.add((file1, file2))

        elif percentage >= similarity_threshold:
            similar.add((file1, file2))

    identical_dir1 = set(os.path.split(file1)[-1] for file1, _ in identical)
    identical_dir2 = set(os.path.split(file2)[-1] for _, file2 in identical)

    print("Identical files:")
    for file1, file2 in identical:
        print(f"{relative_path_resolve(file1)} <-> {relative_path_resolve(file2)}")

    print("\nSimilar files:")
    for file1, file2 in similar:
        similarity = similarity_percentage(file1, file2)
        print(f"{relative_path_resolve(file1)} <-> {relative_path_resolve(file2)}: {similarity:.2f} % similarity")

    print("\nFiles only in", directory1)
    for file in dir1_files:
        if file not in identical_dir2:
            print(relative_path_resolve(file))

    print("\nFiles only in", directory2)
    for file in dir2_files:
        if file not in identical_dir1:
            print(relative_path_resolve(file))


if __name__ == "__main__":
    dir1 = input("Enter first directory path: ")
    dir2 = input("Enter second directory path: ")
    similarity_threshold = float(input("Enter similarity threshold (e.g., 50 for 50 %): "))
    main(dir1, dir2, similarity_threshold)