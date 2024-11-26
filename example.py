import concurrent.futures
from tqdm import tqdm

dictionary = {}
under, grad = None, None
COURSE_ID_UNDERGRAD = ""
api = None
length = 100

with tqdm(total=length) as pbar:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {
            executor.submit(api.get_detailed_user, e.user["id"]): e
            for e in under + grad
        }
        for future in concurrent.futures.as_completed(future_to_url):
            enrollment = future_to_url[future].__dict__
            user_type = enrollment["type"]
            course = (
                "4641"
                if int(enrollment["course_id"]) == int(COURSE_ID_UNDERGRAD)
                else "7641"
            )
            user = enrollment["user"]
            name, sortable_name, short_name = (
                user["name"],
                user["sortable_name"],
                user["short_name"],
            )

            data = future.result()
            email = data["primary_email"]

            dictionary["name"].append(name)
            dictionary["email"].append(email)
            dictionary["course"].append(course)
            dictionary["type"].append(user_type)
            dictionary["sortable_name"].append(sortable_name)
            dictionary["short_name"].append(short_name)

            pbar.update(1)
