
import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/support_system.db"


def get_data(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()


def show_routing_dashboard():

    # Success notification
    if "routing_notice" in st.session_state:
        st.success(st.session_state.routing_notice)
        del st.session_state.routing_notice

    st.title("YottaFlex AI - Customer Support Management")
    st.caption(
        "Intelligent Ticket Routing | SLA Monitoring | Ticket Analytics"
    )

    st.divider()

    # 1. Routing Controls
    st.subheader("Routing Controls")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Run Auto Routing", type="primary", use_container_width=True):
            try:
                from simulation_router import run_simulation

                with st.spinner("Running automatic routing..."):
                    run_simulation()

                st.session_state.routing_notice = (
                    "Automatic routing completed successfully!"
                )
                st.rerun()

            except Exception as e:
                st.error(f"Routing failed: {e}")

    with col2:
        if st.button("Retry Overflow", use_container_width=True):
            try:
                from simulation_router import run_simulation

                with st.spinner("Checking overflow tickets..."):
                    run_simulation()

                st.session_state.routing_notice = (
                    "Overflow routing check completed!"
                )
                st.rerun()

            except Exception as e:
                st.error(f"Overflow retry failed: {e}")

    with col3:
        if st.button("Refresh Dashboard", use_container_width=True):
            st.rerun()

    st.divider()

    # 2. Simulation Overview
    st.subheader("Simulation Overview")

    try:
        tickets = get_data(
            "SELECT COUNT(*) AS total FROM tickets"
        )
        agents = get_data(
            "SELECT COUNT(*) AS total FROM agents"
        )
        assignments = get_data("""
            SELECT COUNT(*) AS total
            FROM simulation_assignments
            WHERE status = 'Active'
        """)
        waiting = get_data("""
            SELECT COUNT(*) AS total
            FROM overflow_queue
            WHERE status = 'Waiting'
        """)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Tickets", f"{int(tickets.iloc[0]['total']):,}")
        c2.metric("Total Agents", f"{int(agents.iloc[0]['total']):,}")
        c3.metric("Active Assignments", f"{int(assignments.iloc[0]['total']):,}")
        c4.metric("Waiting Overflow", f"{int(waiting.iloc[0]['total']):,}")

    except Exception as e:
        st.error(f"Overview error: {e}")

    st.divider()

    # 3. Agent Workload and Capacity
    st.subheader("Agent Workload and Capacity")

    try:
        workload = get_data("""
            SELECT
                a.agent_id,
                a.agent_name,
                a.status,
                a.max_concurrent_tickets,
                COUNT(
                    CASE WHEN sa.status = 'Active' THEN 1 END
                ) AS current_workload
            FROM agents a
            LEFT JOIN simulation_assignments sa
                ON a.agent_id = sa.agent_id
            GROUP BY
                a.agent_id,
                a.agent_name,
                a.status,
                a.max_concurrent_tickets
            ORDER BY current_workload DESC
        """)

        workload["available_capacity"] = (
            workload["max_concurrent_tickets"]
            - workload["current_workload"]
        ).clip(lower=0)

        st.dataframe(
            workload,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Workload error: {e}")

    st.divider()

    # 4. Recent Simulation Assignments
    st.subheader("Recent Simulation Assignments")

    try:
        recent = get_data("""
            SELECT
                simulation_assignment_id,
                ticket_id,
                agent_id,
                assigned_at,
                status
            FROM simulation_assignments
            ORDER BY assigned_at DESC
            LIMIT 20
        """)

        if recent.empty:
            st.info("No simulation assignments available.")
        else:
            st.dataframe(
                recent,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:
        st.error(f"Assignment error: {e}")

    st.divider()

    # 5. Overflow Queue
    st.subheader("Overflow Queue")

    try:
        overflow = get_data("""
            SELECT *
            FROM overflow_queue
            ORDER BY
                CASE status
                    WHEN 'Waiting' THEN 1
                    WHEN 'Simulated' THEN 2
                    ELSE 3
                END
            LIMIT 100
        """)

        if overflow.empty:
            st.info("No overflow tickets available.")
        else:
            st.dataframe(
                overflow,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:
        st.error(f"Overflow error: {e}")

    st.divider()

    # 6. SLA Monitoring
    st.header("SLA Monitoring")

    try:
        sla_summary = get_data("""
            SELECT event_type, COUNT(*) AS total
            FROM sla_events
            GROUP BY event_type
        """)

        met = int(
            sla_summary.loc[
                sla_summary["event_type"] == "Met", "total"
            ].sum()
        )

        breached = int(
            sla_summary.loc[
                sla_summary["event_type"] == "Breached", "total"
            ].sum()
        )

        total_outcomes = met + breached
        compliance = (
            met / total_outcomes * 100
            if total_outcomes else 0
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("SLA Met", f"{met:,}")
        c2.metric("SLA Breached", f"{breached:,}")
        c3.metric("SLA Compliance", f"{compliance:.2f}%")

        st.subheader("SLA Performance Breakdown")

        sla_chart = pd.DataFrame({
            "Tickets": [met, breached]
        }, index=["Met", "Breached"])

        st.bar_chart(sla_chart)

        st.subheader("Recent SLA Breaches")

        breaches = get_data("""
            SELECT
                ticket_id,
                target_at,
                actual_at,
                event_time
            FROM sla_events
            WHERE event_type = 'Breached'
            ORDER BY event_time DESC
            LIMIT 20
        """)

        if breaches.empty:
            st.info("No SLA breaches found.")
        else:
            st.dataframe(
                breaches,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:
        st.error(f"SLA error: {e}")

    st.divider()

    # 7. Ticket Analytics
    st.header("Ticket Analytics Dashboard")

    try:
        status_data = get_data("""
            SELECT status, COUNT(*) AS total
            FROM tickets
            GROUP BY status
            ORDER BY total DESC
        """)

        priority_data = get_data("""
            SELECT priority, COUNT(*) AS total
            FROM tickets
            GROUP BY priority
            ORDER BY total DESC
        """)

        intent_data = get_data("""
            SELECT i.intent_name, COUNT(t.ticket_id) AS total
            FROM tickets t
            LEFT JOIN intents i ON t.intent_id = i.intent_id
            GROUP BY i.intent_name
            ORDER BY total DESC
        """)

        channel_data = get_data("""
            SELECT c.channel_name, COUNT(t.ticket_id) AS total
            FROM tickets t
            LEFT JOIN channels c ON t.channel_id = c.channel_id
            GROUP BY c.channel_name
            ORDER BY total DESC
        """)

        daily_data = get_data("""
            SELECT DATE(created_at) AS ticket_date, COUNT(*) AS total
            FROM tickets
            GROUP BY DATE(created_at)
            ORDER BY ticket_date
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ticket Status Distribution")
            st.bar_chart(status_data.set_index("status"))

        with col2:
            st.subheader("Priority-wise Tickets")
            st.bar_chart(priority_data.set_index("priority"))

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Intent-wise Tickets")
            st.bar_chart(intent_data.set_index("intent_name"))

        with col4:
            st.subheader("Channel-wise Tickets")
            st.bar_chart(channel_data.set_index("channel_name"))

        st.subheader("Daily Ticket Trend")
        st.line_chart(daily_data.set_index("ticket_date"))

    except Exception as e:
        st.error(f"Ticket analytics error: {e}")

    st.divider()

    # 8. Agent Performance Dashboard
    st.header("Agent Performance Dashboard")

    try:
        agent_performance = get_data("""
            SELECT
                a.agent_id,
                a.agent_name,
                a.status AS agent_status,
                a.max_concurrent_tickets AS max_capacity,

                COUNT(DISTINCT sa.ticket_id) AS total_assigned,

                COUNT(DISTINCT CASE
                    WHEN sa.status = 'Active'
                    THEN sa.ticket_id
                END) AS active_assignments,

                COUNT(DISTINCT CASE
                    WHEN sa.status = 'Completed'
                    THEN sa.ticket_id
                END) AS completed_assignments,

                COUNT(DISTINCT CASE
                    WHEN r.resolution_status = 'Resolved'
                    THEN sa.ticket_id
                END) AS assigned_tickets_with_resolution

            FROM agents a

            LEFT JOIN simulation_assignments sa
                ON a.agent_id = sa.agent_id

            LEFT JOIN resolutions r
                ON sa.ticket_id = r.ticket_id

            GROUP BY
                a.agent_id,
                a.agent_name,
                a.status,
                a.max_concurrent_tickets

            ORDER BY total_assigned DESC
        """)

        agent_performance["capacity_utilization"] = (
            agent_performance["active_assignments"]
            / agent_performance["max_capacity"].replace(0, 1)
            * 100
        ).round(2)

        total_assigned = int(
            agent_performance["total_assigned"].sum()
        )

        total_active = int(
            agent_performance["active_assignments"].sum()
        )

        total_completed = int(
            agent_performance["completed_assignments"].sum()
        )

        total_linked_resolved = int(
            agent_performance[
                "assigned_tickets_with_resolution"
            ].sum()
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Assigned", f"{total_assigned:,}")
        c2.metric("Active Assignments", f"{total_active:,}")
        c3.metric("Completed Assignments", f"{total_completed:,}")
        c4.metric("Linked Resolved Records", f"{total_linked_resolved:,}")

        st.subheader("Agent-wise Assignment Performance")

        st.dataframe(
            agent_performance,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Agent Assignment Comparison")

        comparison = agent_performance[
            ["agent_name", "total_assigned", "active_assignments"]
        ].set_index("agent_name")

        st.bar_chart(comparison)

        st.subheader("Agent Capacity Utilization")

        capacity_chart = agent_performance[
            ["agent_name", "capacity_utilization"]
        ].set_index("agent_name")

        st.bar_chart(capacity_chart)

        st.caption(
            "Linked resolved records are tickets with a resolution record "
            "assigned to that agent in the simulation data. This does not "
            "prove which agent personally performed the resolution."
        )

    except Exception as e:
        st.error(f"Agent performance error: {e}")

    st.divider()

    st.caption(
        "YottaFlex AI | Customer Support Ticket Routing and SLA Management"
    )
