from insightspy.SessionCore import RequestCore
import pandas as pd


class PipelinesMixin(RequestCore):
    def pipeline_revisions(self):
        """List available pipelines

        Lists pipelines accessible within the current portal session. Pipeline access is
        limited by user id and the current session project if one is set.

        Returns:
            DataFrame: table of pipeline metadata
        """
        return pd.DataFrame.from_dict(
            self._get("pipelinesDb/project_pipelines_revisions")["response"]["data"]
        )
