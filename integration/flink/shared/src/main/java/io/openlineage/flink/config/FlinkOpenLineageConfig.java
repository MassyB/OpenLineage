/*
/* Copyright 2018-2025 contributors to the OpenLineage project
/* SPDX-License-Identifier: Apache-2.0
*/

package io.openlineage.flink.config;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.openlineage.client.OpenLineageConfig;
import io.openlineage.client.circuitBreaker.CircuitBreakerConfig;
import io.openlineage.client.job.JobConfig;
import io.openlineage.client.run.RunConfig;
import io.openlineage.client.transports.FacetsConfig;
import io.openlineage.client.transports.TransportConfig;
import java.util.Map;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@ToString
public class FlinkOpenLineageConfig extends OpenLineageConfig<FlinkOpenLineageConfig> {

  @JsonProperty("dataset")
  @Setter
  private FlinkDatasetConfig datasetConfig;

  public FlinkOpenLineageConfig() {
    super();
    datasetConfig = new FlinkDatasetConfig();
  }

  public FlinkOpenLineageConfig(
      TransportConfig transportConfig,
      FacetsConfig facetsConfig,
      FlinkDatasetConfig datasetConfig,
      CircuitBreakerConfig circuitBreaker,
      Map metricsConfig,
      RunConfig runConfig,
      JobConfig jobConfig) {
    super(
        transportConfig,
        facetsConfig,
        datasetConfig,
        circuitBreaker,
        metricsConfig,
        runConfig,
        jobConfig);
    this.datasetConfig = datasetConfig;
  }

  @Override
  public FlinkOpenLineageConfig mergeWithNonNull(FlinkOpenLineageConfig other) {
    return new FlinkOpenLineageConfig(
        mergePropertyWith(transportConfig, other.transportConfig),
        mergePropertyWith(facetsConfig, other.facetsConfig),
        mergePropertyWith(datasetConfig, other.datasetConfig),
        mergePropertyWith(circuitBreaker, other.circuitBreaker),
        mergePropertyWith(metricsConfig, other.metricsConfig),
        mergePropertyWith(runConfig, other.runConfig),
        mergePropertyWith(jobConfig, other.jobConfig));
  }
}
