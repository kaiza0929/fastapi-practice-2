<script lang="ts">

import Router from "svelte-spa-router";
import Header from "./components/Header.svelte";
import Home from "./pages/Home.svelte";

const routes = {
	"/": Home
}

</script>

<Header />
<Router routes={routes} />