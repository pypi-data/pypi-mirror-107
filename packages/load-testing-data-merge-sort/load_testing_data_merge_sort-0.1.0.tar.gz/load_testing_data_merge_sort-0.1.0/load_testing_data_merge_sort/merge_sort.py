from typing import List, Union
import click


def merge(left_list: List[Union[int, float]], right_list: List[Union[int, float]]) -> List[Union[int, float]]:
    result = []
    left_index = right_index = 0

    len_left, len_right = len(left_list), len(right_list)

    for _ in range(len_left + len_right):
        if left_index != len_left and right_index != len_right:
            if left_list[left_index] <= right_list[right_index]:
                result.append(left_list[left_index])
                left_index += 1
            else:
                result.append(right_list[right_index])
                right_index += 1

        elif left_index == len_left:
            result.append(right_list[right_index])
            right_index += 1

        elif right_index == len_right:
            result.append(left_list[left_index])
            left_index += 1

    return result


@click.command()
@click.argument('data', nargs=-1, required=True)
def merge_sort(data):
    data = [int(i) for i in data if i != '']
    if len(data) <= 1:
        return data

    mid = len(data) // 2

    left_list = merge_sort(data[:mid])
    right_list = merge_sort(data[mid:])

    return merge(left_list, right_list)


if __name__ == "__main__":
    merge_sort()
