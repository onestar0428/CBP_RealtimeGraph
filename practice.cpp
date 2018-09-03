#include<iostream>
#include<vector>

#define cell 0
#define area -1
#define camera1 1
#define camera2 2
#define camera3 3
#define camera4 4
#define camera5 5
#define wall 6

using namespace std;

int count(vector<vector<int>> arr) {
	int cnt = 0;

	for (int i = 0; i<arr.size(); i++) {
		for (int j = 0; j<arr[i].size(); j++) {
			if (arr[i][j] == cell) {
				cnt++;
			}
		}
	}
	return cnt;
}

int map(vector<vector<int>> arr, vector<int> x, vector<int> y) {
	for (int i = 0; i<x.size(); i++) {
		switch (arr[i][j]) {
		case camera1:
			break;
		case camera2:
			break;
		case camera3:
			break;
		case camera4:
			break;
		case camera5:
			break;
		}
	}
}

int main() {
	int n, m;
	cin >> n >> m;
	vector<vector<int>> arr(n, vector<int>(m, 0));
	vector<int> loc_x;
	vector<int> loc_y;

	int result = 0;
	for (int i = 0; i<n; i++) {
		for (int j = 0; j<m; j++) {
			cin >> arr[i][j];
			if (arr[i][j] == cell) {
				result++;
			}
			else if (arr[i][j] == camera1
				|| arr[i][j] == camera2
				|| arr[i][j] == camera3
				|| arr[i][j] == camera4
				|| arr[i][j] == camera5) {
				loc_x.push_back(i);
				loc_y.push_back(j);
			}
		}
	}

	return 0;
}
#include<iostream>
#include<vector>

#define x 0
#define y 1
#define d 2
#define g 3

#define map_size 100

#define right 0
#define up 1
#define left 2
#define down 3

using namespace std;

int count(vector<vector<int>> map) {
	int cnt = 0;
	for (int i = 0; i < map_size; i++) {
		for (int j = 0; j < map_size; j++) {
			if (map[i][j] == 1) {
				if (map[i + 1][j] == 1 && map[i][j + 1] == 1 && map[i + 1][j + 1] == 1) {
					cnt++;
				}
			}
		}
	}
	return cnt;
}

vector<vector<int>> draw(vector<vector<int>> arr, int n) {
	vector<vector<int>> map(map_size, vector<int>(map_size, 0));
	vector<vector<int>> path(n);

	int flag = 1, gen = 0;
	for (int i = 0; i < n; i++) {
		path[i].push_back(arr[i][d]);
		map[arr[i][y]][arr[i][x]] = 1;
		switch (arr[i][d]) {
		case right:
			arr[i][x]++;
			break;
		case up:
			arr[i][y]--;
			break;
		case left:
			arr[i][x]--;
			break;
		case down:
			arr[i][y]++;
			break;
		}
		map[arr[i][y]][arr[i][x]] = 1;
	}
	gen++;

	while (flag) {
		flag = 0;
		for (int i = 0; i < n; i++) {
			if (gen == 1) {
				flag = 1;
				path[i].push_back((path[i][path[i].size() - 1] + 1) % 4);
			}
			else if (arr[i][g] >= gen) {
				flag = 1;
				int tmp_size = path[i].size();
				for (int j = 0; j < tmp_size; j++) {
					path[i].push_back(path[i][j]);
				}
				for (int j = tmp_size; j < tmp_size + tmp_size / 2; j++) {
					path[i][j] = (path[i][j] + 2) % 4;
				}
			}
			if (flag == 1 && arr[i][g] >= gen) {
				for (int j = path[i].size() / 2; j < path[i].size(); j++) {
					switch (path[i][j]) {
					case right:
						arr[i][x]++;
						break;
					case up:
						arr[i][y]--;
						break;
					case left:
						arr[i][x]--;
						break;
					case down:
						arr[i][y]++;
						break;
					}
					map[arr[i][y]][arr[i][x]] = 1;
				}
			}
		}
		gen++;
	}

	return map;
}

int main() {
	int n;
	cin >> n;

	vector<vector<int>> arr(n, vector<int>(4, 0));
	for (int i = 0; i < n; i++) {
		cin >> arr[i][x] >> arr[i][y] >> arr[i][d] >> arr[i][g];
	}

	cout << count(draw(arr, n)) << endl;
	return 0;
}
