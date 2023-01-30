import unittest
import numpy as np
import numpy.testing as npt
import pandas as pd

import os


from tercen.client import context as ctx
import tercen.util.builder as bld
from operator_funcs import fit_phate


class TestOperator(unittest.TestCase):
    def setUp(self):
        envs = os.environ
        if 'TERCEN_USERNAME' in envs:
            username = envs['TERCEN_USERNAME']
        else:
            username = None

        if 'TERCEN_PASSWORD' in envs:
            passw = envs['TERCEN_PASSWORD']
        else:
            passw = None

        if 'TERCEN_URI' in envs:
            serviceUri = envs['TERCEN_URI']
        else:
            serviceUri = None


        self.wkfBuilder = bld.WorkflowBuilder()
        self.wkfBuilder.create_workflow( 'python_auto_project', 'python_workflow')
        self.wkfBuilder.add_table_step( './data/scRNAseq_large_by25_no0.csv' )

        self.wkfBuilder.add_data_step(yAxis={"name":"Count", "type":"double"}, 
                        columns=[{"name":"GeneID", "type":"string"}],
                        rows=[{"name":"Seq", "type":"string"}])

        if username is None: # Running locally
            self.context = ctx.TercenContext(
                            stepId=self.wkfBuilder.workflow.steps[1].id,
                            workflowId=self.wkfBuilder.workflow.id)
        else: # Running from Github Actions
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
        resDf = self.context.save_dev(df)
        
      
        assert( not resDf is None )
        assert(resDf.shape == df.shape)
        for i in range(0, len(resDf.columns)):
            c0 = df.columns[i] 
            c1 = resDf.columns[i] 
            
            assert(c0 == c1)
            npt.assert_array_almost_equal(df[c0].values, resDf[c1].values)


if __name__ == '__main__':
    unittest.main()