<script lang="ts">

import axios from "axios";

type Movie = {
	id: string;
	name: string;
}

let userId: number | null = null;
let movies: Movie[] = [];
let message: string = "";

const getMovies = async (userId: number): Promise<Movie[]> => {
	
	if (userId === null) {
		message = "ユーザーIDが未入力です";
		return [];
	} else if (isNaN(userId) === true) {
		message = "入力が不正です";
		return [];
	} else {
        message = "";
    }
	const res = await axios.get(`http://localhost:8000/api/collaborative?userId=${userId}`);
	return res.data.movies;

}

</script>


<main>
	<div>
        <div class="mb-3">
            <label for="userId">ユーザーID</label>
            <input id="userID" bind:value={userId} class="form-control">
        </div>
		<button class="btn btn-primary"  on:click={() => {
			getMovies(userId).then((m) => {
				/* 変数の再代入しか再レンダリングを実行しない仕様になっている */
				movies = movies.concat(m);
			});
		}}>おすすめ映画を検索する</button>
	</div>
    <div>
        <p>{message}</p>
    </div>
	<div>
		<table>
			<thead>
				<tr>
					<th>映画ID</th>
					<th>映画タイトル</th>
                </tr>
			</thead>
			<tbody>
				{#each [...movies] as movie}
					<tr>
						<td>{movie.id}</td>
						<td>{movie.name}</td>
                    </tr>
				{/each}
			</tbody>
		</table>
	</div>
</main>