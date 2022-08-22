import modules.secretary as secr
import modules.visualizer as vis
import modules.engineer as eng


class ProductionMonitor:
    def __init__(self):
        pass

    def do(self):
        production = secr.load_production_update()

        vis.print_null(production)

        tmp = eng.prepare_for_model(production, 1)
        tmp.reset_index(inplace=True, drop=True)

        errors = [-1.0, "UNKNOWN"]

        print("\n- Check invalid values")

        for feature in tmp.columns:
            print_me = tmp.loc[tmp[feature].isin([errors])]

            if len(print_me) > 0:
                print(f"{feature:} contains {errors} : {len(print_me)}")

        secr.save_model(tmp)
