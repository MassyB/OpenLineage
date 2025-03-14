/*
/* Copyright 2018-2025 contributors to the OpenLineage project
/* SPDX-License-Identifier: Apache-2.0
*/

package io.openlineage.client;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import io.openlineage.client.OpenLineage.DatasetEvent;
import io.openlineage.client.OpenLineage.JobEvent;
import io.openlineage.client.OpenLineage.RunEvent;
import io.openlineage.client.circuitBreaker.CircuitBreaker;
import io.openlineage.client.circuitBreaker.CircuitBreakerState;
import io.openlineage.client.transports.Transport;
import org.junit.jupiter.api.Test;

class OpenLineageClientTest {

  CircuitBreaker circuitBreaker = mock(CircuitBreaker.class);
  Transport transport = mock(Transport.class);
  MeterRegistry meterRegistry = new SimpleMeterRegistry();
  OpenLineageClient client = new OpenLineageClient(transport, circuitBreaker, meterRegistry);

  @Test
  void testCircuitBreakerFroEmitRunEvent() {
    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(true));
    client.emit(mock(RunEvent.class));
    verify(transport, times(0)).emit(any(RunEvent.class));

    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(false));
    client.emit(mock(RunEvent.class));
    verify(transport, times(1)).emit(any(RunEvent.class));
  }

  @Test
  void testCircuitBreakerFroEmitJobEvent() {
    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(true));
    client.emit(mock(JobEvent.class));
    verify(transport, times(0)).emit(any(JobEvent.class));

    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(false));
    client.emit(mock(JobEvent.class));
    verify(transport, times(1)).emit(any(JobEvent.class));
  }

  @Test
  void testCircuitBreakerFroEmitDatasetEvent() {
    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(true));
    client.emit(mock(DatasetEvent.class));
    verify(transport, times(0)).emit(any(DatasetEvent.class));

    when(circuitBreaker.currentState()).thenReturn(new CircuitBreakerState(false));
    client.emit(mock(DatasetEvent.class));
    verify(transport, times(1)).emit(any(DatasetEvent.class));
  }
}
