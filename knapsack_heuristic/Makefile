define run_knapsack_heuristic
	for i in NK ZKC ZKW; do
		for j in 4 10 15 20 22; do
			i_file="data/input/$${i}/$${i}$${j}_inst.dat"
			s_file="data/input/$${i}/$${i}$${j}_sol.dat"
			echo $${i_file}
			echo $${s_file}
			if ! ./knapsack_heuristic.py $${i_file} $${s_file} -v $1; then
				exit 0
			fi
			echo "--------------------"
		done
	done
endef

.ONESHELL:
brute_force:
	$(call run_knapsack_heuristic,bf)

.ONESHELL:
branch_n_bound:
	$(call run_knapsack_heuristic,bb)

.ONESHELL:
dynamic:
	$(call run_knapsack_heuristic,dp)

.ONESHELL:
greedy:
	$(call run_knapsack_heuristic,gh)

.ONESHELL:
redux:
	$(call run_knapsack_heuristic,rgh)

.ONESHELL:
fptas:
	$(call run_knapsack_heuristic,fptas)
