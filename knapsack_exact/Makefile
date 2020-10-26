define run_knapsack_exact
	for i in 4 10 15 20 22; do
		i_file="data/input/$(1)R/$(1)R$${i}_inst.dat"
		s_file="data/input/$(1)R/$(1)K$${i}_sol.dat"
		echo $${i_file}
		echo $${s_file}
		if ! ./knapsack_exact.py $${i_file} $${s_file} $2; then
			exit 0
		fi
		echo "--------------------"
	done
endef

.ONESHELL:
ke_nr_bf:
	$(call run_knapsack_exact,N)

.ONESHELL:
ke_nr_bb:
	$(call run_knapsack_exact,N,-b)

.ONESHELL:
ke_zr_bf:
	$(call run_knapsack_exact,Z)

.ONESHELL:
ke_zr_bb:
	$(call run_knapsack_exact,Z,-b)
