import frappe
from frappe import get_doc, get_list, get_all
from frappe.sessions import Session
from flask import stream_with_context
from flask import Response

@frappe.whitelist()
def retrieve_podcasts(search=None, page=None, limit=None):
    filters = {}
    if search:
        filters["title"] = ["like", f"%{search}%"]

    podcasts = get_list(
        "Podcast",
        filters=filters,
        fields=["name", "title", "host", "description", "cover_image_url", "audio_file_url", "release_date",
                "average_rating", "num_ratings", "subscription_level"],
        or_filters=[],
        limit_page_length=limit,
        start=page * limit if page and limit else None
    )

    total_count = get_all(
        "Podcast",
        filters=filters,
        fields=["count(*) as total_count"]
    )[0].total_count

    # Get the currently logged-in user
    session = frappe.session.user
    user_favorite_podcasts = get_list(
        "User Favorite",
        filters={"user": session},
        fields=["audio_content"],
    )

    favorite_podcast_ids = [fav.audio_content for fav in user_favorite_podcasts]

    for podcast in podcasts:
        podcast["is_favorite"] = podcast["name"] in favorite_podcast_ids

    response = {
        "podcasts": podcasts,
        "total_count": total_count
    }

    return response

@frappe.whitelist()
def retrieve_podcast(podcast_id):
    podcast = get_doc("Podcast", podcast_id)

    response = {
        "id": podcast.name,
        "title": podcast.title,
        "host": podcast.host,
        "description": podcast.description,
        "cover_image_url": podcast.cover_image_url,
        "audio_file_url": podcast.audio_file_url,
        "release_date": podcast.release_date,
        "average_rating": podcast.average_rating,
        "num_ratings": podcast.num_ratings,
        "subscription_level": podcast.subscription_level
    }

    # Get the currently logged-in user
    session = frappe.session.user
    user_favorite_podcast = get_doc(
        "User Favorite",
        filters={"user": session, "audio_content": podcast_id}
    )

    response["is_favorite"] = bool(user_favorite_podcast)

    return response

@frappe.whitelist(allow_guest=True)
def retrieve_podcast_sample(podcast_id):
    podcast = get_doc("Podcast", podcast_id)
    subscription_level = podcast.subscription_level

    # Check if the user has access to the episodes based on the subscription level
    if check_subscription_access(subscription_level):
        # You need to implement the logic to retrieve the sample audio file URL based on the podcast ID
        sample_audio_url = get_file_url(podcast_id)

        # Define a generator function to stream the audio file
        def generate_audio():
            with open(sample_audio_url, 'rb') as audio_file:
                while True:
                    chunk = audio_file.read(4096)
                    if not chunk:
                        break
                    yield chunk

        # Use the stream_with_context function to stream the audio file
        return Response(stream_with_context(generate_audio()), content_type='audio/mp3')
    else:
        raise frappe.PermissionError("You don't have access to this podcast's episodes.")
    
@frappe.whitelist(allow_guest=True)
def get_episodes_of_podcast(podcast_id):
    podcast = get_doc("Podcast", podcast_id)
    subscription_level = podcast.subscription_level

    # Check if the user has access to the episodes based on the subscription level
    if check_subscription_access(subscription_level):
        episodes = get_list(
            "Podcast Episode",
            filters={"podcast": podcast_id},
            fields=["name", "title", "description", "episode_number", "air_date", "audio_file", "total_listening_time"]
        )
        return episodes
    else:
        raise frappe.PermissionError("You don't have access to this podcast's episodes.")

@frappe.whitelist(allow_guest=True)
def get_audio_file_for_episode(podcast_id, episode_id):
    podcast = get_doc("Podcast", podcast_id)
    subscription_level = podcast.subscription_level

    # Check if the user has access to the episodes based on the subscription level
    if check_subscription_access(subscription_level):
        episode = get_doc("Podcast Episode", episode_id)

        # You need to implement the logic to retrieve the audio file URL for the episode based on the podcast and episode IDs
        audio_file_url = get_file_url(podcast_id, episode_id)

        # Define a generator function to stream the audio file
        def generate_audio():
            with open(audio_file_url, 'rb') as audio_file:
                while True:
                    chunk = audio_file.read(4096)
                    if not chunk:
                        break
                    yield chunk

        # Use the stream_with_context function to stream the audio file
        return Response(stream_with_context(generate_audio()), content_type='audio/mp3')
    else:
        raise frappe.PermissionError("You don't have access to this episode.")

def check_subscription_access(subscription_level):
    # Get the currently logged-in user
    session = frappe.session.user

    # Retrieve the subscription level of the user
    user_subscription_level = get_user_subscription_level(session)

    # Compare the user's subscription level with the required subscription level for accessing the podcast episodes
    if user_subscription_level >= subscription_level:
        return True
    else:
        return False

def get_user_subscription_level(user):
    user_subscription = get_doc("User Subscription", filters={"user": user}, fields=["subscription_level"])
    if user_subscription:
        return user_subscription.subscription_level
    else:
        return None

@frappe.whitelist()
def update_user_listening_history(user, audio_content, start_time, end_time):
    total_listening_time = calculate_total_listening_time(start_time, end_time)
    create_user_listening_history(user, audio_content, start_time, end_time, total_listening_time)
    update_podcast_episode_total_listening_time(audio_content, total_listening_time)
    update_podcast_total_listening_time(audio_content, total_listening_time)

def calculate_total_listening_time(start_time, end_time):
    # Implementation logic to calculate the total listening time based on the start and end time
    # You can replace this with your own implementation
    total_time = end_time - start_time
    return total_time

def create_user_listening_history(user, audio_content, start_time, end_time, total_listening_time):
    user_listening_history = frappe.new_doc("User Listening History")
    user_listening_history.user = user
    user_listening_history.audio_content = audio_content
    user_listening_history.start_time = start_time
    user_listening_history.end_time = end_time
    user_listening_history.total_listening_time = total_listening_time
    user_listening_history.insert()

def update_podcast_episode_total_listening_time(audio_content, total_listening_time):
    episodes = get_list(
        "Podcast Episode",
        filters={"podcast": audio_content},
        fields=["name"]
    )

    for episode in episodes:
        episode_doc = get_doc("Podcast Episode", episode.name)
        episode_doc.total_listening_time += total_listening_time
        episode_doc.save()

def update_podcast_total_listening_time(audio_content, total_listening_time):
    podcast = get_doc("Podcast", audio_content)
    podcast.total_listening_time += total_listening_time
    podcast.save()

def get_file_url(file_name):
    if file_name:
        file_doc = frappe.get_doc("File", file_name)
        return file_doc.file_url
    else:
        return None