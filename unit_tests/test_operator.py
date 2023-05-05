import unittest
import numpy as np
import numpy.testing as npt
import pandas as pd

import os


from tercen.client import context as ctx
import tercen.util.helper_functions as utl
import tercen.util.builder as bld
from operator_funcs import fit_phate


class TestOperator(unittest.TestCase):
    def setUp(self):
        envs = os.environ
        isLocal = False
        if 'TERCEN_PASSWORD' in envs:
            passw = envs['TERCEN_PASSWORD']
        else:
            passw = None

        if 'TERCEN_URI' in envs:
            serviceUri = envs['TERCEN_URI']
        else:
            serviceUri = None
        if 'TERCEN_USERNAME' in envs:
            username = envs['TERCEN_USERNAME']
        else:
            isLocal = True
            username = 'test'
            passw = 'test'
            conf = {}
            with open("./unit_tests/env.conf") as f:
                for line in f:
                    if len(line.strip()) > 0:
                        (key, val) = line.split(sep="=")
                        conf[str(key)] = str(val).strip()

            serviceUri = ''.join([conf["SERVICE_URL"], ":", conf["SERVICE_PORT"]])

        self.wkfBuilder = bld.WorkflowBuilder()
        self.wkfBuilder.create_workflow( 'python_auto_project', 'python_workflow')
        self.wkfBuilder.add_table_step( './data/scRNAseq_large_by25_no0.csv' )

        self.wkfBuilder.add_data_step(yAxis={"name":"Count", "type":"double"}, 
                        columns=[{"name":"GeneID", "type":"string"}],
                        rows=[{"name":"Seq", "type":"string"}])

        self.context = ctx.TercenContext(
                        username=username,
                        password=passw,
                        serviceUri=serviceUri,
                        stepId=self.wkfBuilder.workflow.steps[1].id,
                        workflowId=self.wkfBuilder.workflow.id)

        self.addCleanup(self.clear_workflow)
        
    def clear_workflow(self):
        self.wkfBuilder.clean_up_workflow()

    def test_row_col(self) -> None:
        df = fit_phate(self.context)
        df = self.context.add_namespace(df)
        
        dfRel = utl.as_relation(df)
        dfJoin = utl.as_join_operator(dfRel, self.context.cnames, 
                        self.context.cnames)

        
        
        resDf = self.context.save_relation_dev(dfJoin) 
        
        # NOTE
        # save_dev always return .ci and .ri columns, though they will not be present in the resulting table if all values are equal to 0
        resDf.drop(".ri", inplace=True, axis=1)

        assert( not resDf is None )
        assert(resDf.shape == df.shape)
        for i in range(0, len(resDf.columns)):
            c0 = df.columns[i] 
            c1 = resDf.columns[i] 
            
            assert(c0 == c1)
            npt.assert_array_almost_equal(df[c0].values, resDf[c1].values)


if __name__ == '__main__':
    unittest.main()